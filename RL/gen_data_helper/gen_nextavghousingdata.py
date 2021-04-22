import os
print(os.getcwd())
import numpy as np 
np.random.seed(7)

import math

import copy 
import pandas as pd
import time
import datetime

from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from tslearn.clustering import TimeSeriesKMeans

idx="1"
KM_file= '../Demo/ECEMasterProject/models/KM/KM1.h5'
PATH = f"../Demo/ECEMasterProject/RL/Data/Avg_House_{idx}/"
Dataset = '../Demo/ECEMasterProject/15minute_data_newyork/15minute_data_newyork.csv'
solarmodel_file = '../Demo/ECEMasterProject/models/LSTM_Solar/LSTM_solar_house_model_1_51_adam.h5'
nonsolarmodel_file = '../Demo/ECEMasterProject/models/LSTM_nonsolar/house_model_0_77_adam.h5'

print(KM_file +"_"+ str(os.path.exists(KM_file)))
print(PATH +"_"+ str(os.path.exists(PATH)))
print(Dataset +"_"+ str(os.path.exists(Dataset)))
print(solarmodel_file +"_"+ str(os.path.exists(solarmodel_file)))
print(nonsolarmodel_file +"_"+ str(os.path.exists(nonsolarmodel_file)))


def convertDate(d):
    d = pd.to_datetime(d[:-3])
    return d 

def create_dataset(dataset, look_back=1, look_ahead=None):
	"function for creating dataset for model, X being the known data, and Y being target data"
	if look_ahead is None:
		look_ahead = look_back
	dataX, dataY = [], []
	for i in range(len(dataset)-2*look_back):
		dataX.append(dataset[i:(i+look_back), 0])
		if look_ahead == 0:
			dataY.append(dataset[i + look_back, 0])
		else:
			dataY.append(dataset[(i+look_back):(i+look_back+look_ahead), 0])
		
	return np.array(dataX), np.array(dataY)

def dataset_per_house(house, look_back = 96):
    dataframe = house['grid']
    dataset = np.matrix(dataframe.values).transpose()
    dataset = dataset.astype('float32')

    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    print(len(dataset)) #just to somewhat prove that the dataset aren't the same
    train_size = int(len(dataset) * 0.67)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size:,:]
    # look_back = 96 #(60mins/15min)*24 hours
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))
    return trainX, trainY, testX, testY, dataset, scaler

def get_avg_day(look_back =96,  house = 0, absolute = False):

    dataframe = housing_data[house]['grid']
    fulldays=len(dataframe)//look_back
    grid_data=dataframe.to_numpy()

    grid_day_matrix=grid_data[:(look_back*fulldays)].reshape(-1, look_back)
    if absolute == True:
        grid_day_matrix = abs(grid_day_matrix)
    #avg house0 grid data 
    avg_house_grid=np.mean(grid_day_matrix, axis=0)
    # print(grid_day_matrix.shape)
    return avg_house_grid

def get_avg_day_from_predict(data, look_back =96, absolute = False):
    grid_day_matrix= data[::look_back]
    if absolute == True:
        grid_day_matrix = abs(grid_day_matrix)
    #avg house0 grid data 
    avg_house_grid=np.mean(grid_day_matrix, axis=0)
    return avg_house_grid

def reshape_stack_reshapeX(X): 
    r,c,z=X[0].shape
    x0 = X[0].reshape(r,c)
    for i, x in enumerate(X):
        if i == 0:
            continue
        r,c,z = x.shape 
        x = x.reshape(r,c)

        x0 = np.vstack((x0,x))
    # print(x0.shape)
    r,c= x0.shape
    x0 = x0.reshape(r,c,1)
    return x0

def reshape_stack_reshapeY(Y, starting_point = 0):     
    y0 = Y[0]
    # print(y0.shape)
    scaler_mapper = (np.zeros(y0.shape) + starting_point)
    for i, y in enumerate(Y):
        if i == 0:
            continue
        scaler_mapper_next = (i*np.ones(y.shape) + starting_point)
        scaler_mapper = np.vstack((scaler_mapper,scaler_mapper_next))
        y0 = np.vstack((y0,y))
    # r,c,= y0.shape
    # y0 = y0.reshape(r,c)
    # print(y0.shape)
    return y0, scaler_mapper

def reshape_stack_reshapedata(data):
    
    r,c = data[0].shape
    # print()
    data0 = data[0].reshape(r)
    # scaler_mapper = [(np.zeros(data0.shape) + starting_point).flatten()]
    for i, points in enumerate(data):
        if i == 0:
            continue
        # points = points.flatten()
        r,c = points.shape
        points = points.reshape(r)
        # scaler_mapper.append((i*np.ones(points.shape) + starting_point).flatten())
        data0 = np.hstack((data0,points))
    # # r, = data0.shape
    # print(data0.shape)
    # data0 = data0.reshape(r,1)
    data0 = data0.transpose()
    # print(data0.shape)
    
    return data0

def unscale_per_house(listofscales, scalemap, data, lookback = 96):
    # print(data.shape)
    unscaled_data = []
    for i,row in enumerate(scalemap):
        # print(i)
        # print(row[-1])
        # if i in [1,2,3,4,5]:
        #     print(data[i].shape)
        unscaled_data.append(listofscales[int(row[0])].inverse_transform(data[i].reshape(1, -1)).reshape(lookback,))
    unscaled_data = np.array(unscaled_data)
    # print(unscaled_data.shape)
    return unscaled_data

def get_avg_day_pred(model, look_back =96,  house = 0):
    scaler = MinMaxScaler(feature_range=(0, 1))

    dataframe = housing_data[house]['grid']
    dataset = np.matrix(dataframe.values).transpose()
    dataset = dataset.astype('float32')
    dataset = scaler.fit_transform(dataset)
    
    
    house0X, house0Y = create_dataset(dataset, look_back)
    house0X = house0X.reshape(house0X.shape[0], house0X.shape[1],1)
    house0Predict = model.predict(house0X)
    house0Predict = scaler.inverse_transform(house0Predict)
    house0Y = scaler.inverse_transform(house0Y)
    train0Score = math.sqrt(mean_squared_error(house0Y, house0Predict))

    pred_house0_matrix=house0Predict[::look_back]
    
    #avg house0 grid data 
    pred_house0_grid=np.mean(pred_house0_matrix, axis=0)
    # print(grid_day_matrix.shape)
    return pred_house0_grid, train0Score
    
if __name__ == "__main__":
    fulldata = pd.read_csv(Dataset) 
    data=fulldata[['dataid','local_15min','grid']]
    sorteddata=data.sort_values(by = ['dataid', 'local_15min'])
    ids=sorteddata['dataid'].unique().tolist()

    housing_data = []
    for i in range(len(ids)):
        housing_data.append(sorteddata.loc[sorteddata.dataid==ids[i]])
        housing_data[i] = housing_data[i].reset_index().drop(columns=['index'])

    avg_house_list = []
    for i in range(len(housing_data)):
        avg_house_list.append(get_avg_day(house= i))
    np_avg_house = np.asarray(avg_house_list) 
    r,c =np_avg_house.shape
    np_avg_house_3d = np.reshape(np_avg_house,(r,c,1))

    KMmodel=TimeSeriesKMeans.from_hdf5(KM_file)
    houseclasses= KMmodel.predict(np_avg_house_3d)

    solarhouses0 = []
    nonsolarhouses1 = []
    solarmodel = load_model(solarmodel_file)
    nonsolarmodel = load_model(nonsolarmodel_file)

    for i, classes in enumerate(houseclasses): 
        if classes==0:
            # solarhouses0.append(housing_data[i])
            pred_house0_grid, train0Score = get_avg_day_pred(solarmodel, look_back =96,  house = i)
            np.save(PATH+'solarhouse/'+f'{i}', pred_house0_grid, allow_pickle=False)
        else: 
            # nonsolarhouses1.append(housing_data[i])
            pred_house0_grid, train0Score = get_avg_day_pred(nonsolarmodel, look_back =96,  house = i)
            np.save(PATH+'nonsolarhouse/'+f'{i}', pred_house0_grid, allow_pickle=False)

    # numofsolarhouses = len(solarhouses0)
    # numofnonsolarhouses = len(nonsolarhouses1)
    # numbertrainingsolarhouse=int(numofsolarhouses * 2/3)
    # numbertraininghouse=int(numofnonsolarhouses * 3/4)
    
    # listoftrainX = []
    # listoftrainY =[]
    # listoftestX = []
    # listoftestY = []
    # listofdataset = []
    # listofscaler = []
    # for i in range(numbertraininghouse ):
    #     trainX, trainY, testX, testY, dataset, scaler =dataset_per_house(nonsolarhouses1[i])
    #     listoftrainX.append(trainX)
    #     listoftrainY.append(trainY)
    #     listoftestX.append(testX)
    #     listoftestY.append(testY)
    #     listofdataset.append(dataset)
    #     listofscaler.append(scaler)

    # #get val data

    # listofvaltrainX = []
    # listofvaltrainY =[]
    # listofvaltestX = []
    # listofvaltestY = []
    # listofvaldataset = []
    # # listofvalscalersolar = []
    # for i in range(numbertraininghouse, numofnonsolarhouses):
    #     trainX, trainY, testX, testY, dataset, scaler=dataset_per_house(nonsolarhouses1[i])
    #     listofvaltrainX.append(trainX)
    #     listofvaltrainY.append(trainY)
    #     listofvaltestX.append(testX)
    #     listofvaltestY.append(testY)
    #     listofvaldataset.append(dataset)
    #     listofscaler.append(scaler)

    # trainX = reshape_stack_reshapeX(listoftrainX)
    # trainY, train_scaler_mapper = reshape_stack_reshapeY(listoftrainY)
    # testX = reshape_stack_reshapeX(listoftestX)
    # testY, test_scaler_mapper = reshape_stack_reshapeY(listoftestY)
    # dataset  = reshape_stack_reshapedata(listofdataset)

    # valtrainX = reshape_stack_reshapeX(listofvaltrainX)
    # valtrainY, valtrain_scaler_mapper = reshape_stack_reshapeY(listofvaltrainY, train_scaler_mapper[-1][0]+1)
    # valtestX = reshape_stack_reshapeX(listofvaltestX)
    # valtestY, valtest_scaler_mapper = reshape_stack_reshapeY(listofvaltestY, test_scaler_mapper[-1][0]+1)
    # valdataset = reshape_stack_reshapedata(listofvaldataset)
    print('Complete')


