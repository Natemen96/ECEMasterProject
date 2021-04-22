import os
import numpy as np 
np.random.seed(7)
import pandas as pd

from tslearn.clustering import TimeSeriesKMeans


KM_file= '../Demo/ECEMasterProject/models/KM/KM1.h5'
PATH = "../Demo/ECEMasterProject/RL/Data/Avg_House/"
Dataset = r'../Demo/ECEMasterProject/15minute_data_newyork/15minute_data_newyork.csv'

def convertDate(d):
    d = pd.to_datetime(d[:-3])
    return d 

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
    for i, classes in enumerate(houseclasses): 
        if classes==0:
            # solarhouses0.append(housing_data[i])
            np.save(PATH+'solarhouse/'+f'{i}', avg_house_list[i], allow_pickle=False)
        else: 
            # nonsolarhouses1.append(housing_data[i])
            np.save(PATH+'nonsolarhouse/'+f'{i}', avg_house_list[i], allow_pickle=False)

    # numofsolarhouses = len(solarhouses0)
    # numofnonsolarhouses = len(nonsolarhouses1)

    print('Complete')


