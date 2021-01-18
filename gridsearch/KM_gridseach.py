import numpy as np 
import matplotlib.dates as mdates
import pandas as pd
import time
import multiprocessing

from sklearn.model_selection import cross_validate, train_test_split, cross_val_score, GridSearchCV, ParameterGrid

import filterpy.kalman as kf 

Dataset = r'ECEMasterProject\15minute_data_newyork\15minute_data_newyork.csv'
fulldata = pd.read_csv(Dataset) 
data=fulldata[['dataid','local_15min','grid']]
sorteddata=data.sort_values(by = ['dataid', 'local_15min'])
ids=sorteddata['dataid'].unique().tolist()
housing_data = []

def convertDate(d):
    d = pd.to_datetime(d[:-3])
    return d 

for i in range(len(ids)):
    housing_data.append(sorteddata.loc[sorteddata.dataid==ids[i]])
    housing_data[i] = housing_data[i].reset_index().drop(columns=['index'])
    housing_data[i]['local_15min'] = housing_data[i]['local_15min'].apply(convertDate)
    #Convert datetimes to ints for regession 
    housing_data[i]['15min_ints'] =  housing_data[i]['local_15min'].map(mdates.date2num)

#KM 
df = pd.DataFrame(housing_data[0], columns=['15min_ints','grid']).set_index('15min_ints')

train_df = df.iloc[:-900, :]
test_df = df.iloc[-900:, :]

true_df = housing_data[0].drop(housing_data[0].index[0])

grid_params = {
    'Q': np.arange(1,51),
    'array_limit': np.arange(1, 31) 
}
grid = list(ParameterGrid(grid_params))

class KalmanMain: 
    def __init__(self,data, array_limit = 120, Q = 9e15):
        "define inits values"
        self.mean = data 

        #save observations
        self.obs_vals = list()
        self.obs_vals.append(data)
        
        #array limit is tunable 
        self.array_limit = array_limit

        self.Q = Q #Tunable 

    def get_meaurement_var(self, data):
        "update var based on fixed list of vals"
        self.obs_vals.append(data)
        num_of_obs = len(self.obs_vals)
        if num_of_obs > self.array_limit:
            #remove 1st item to make room for more data 
            self.obs_vals.pop(0)
        return np.var(self.obs_vals)

    def clear(self, data):
        "clear object for new kalman filter"
        self.mean = data
        self.obs_vals = list()
        self.obs_vals.append(data)
    def kalman_main(self, list_of_vars, added_list = list()):
        "main function for kalman"
        residual = list() #residual is the difference between the prediction and the actual measurement
        prediction = list() 
        estimation = list() #estimation is the updated prediction based on the seen measurement
        for index, measure in enumerate(list_of_vars+added_list):
            if index == 0:
                mvar = self.get_meaurement_var(measure)  
                var = np.var(list_of_vars) #get total var
                x, P = kf.predict(x=measure,P=var, Q=self.Q) 
                prediction.append(x)
                x, P = kf.update(x=x, P=P, z = measure, R=self.get_meaurement_var(measure))
                estimation.append(x)
            else:
                residual.append(abs(prediction[index-1]-measure))
                x, P = kf.predict(x=x, P=P, Q=self.Q)
                prediction.append(x)
                x, P = kf.update(x=x, P=P, z=measure, R=self.get_meaurement_var(measure))
                estimation.append(x)
        return residual, prediction, estimation


def evaluate_single(args):
    index, params = args
    print('Evaluating params: {}'.format(params))
    params = {**params}
    
    Kalmain = KalmanMain(train_df.iloc[0],**params )
    residual, prediction, estimation = Kalmain.kalman_main(list(train_df.values), list(test_df.values) )
    # pred = HWES(train_df, trend="add", seasonal="add", **params).fit().forecast(900)
    
    score = np.sqrt(np.mean(np.square( residual )))

    print('Finished evaluating set {} with score of {}.'.format(index, score))
    return score

def run():
    start_time = time.time()
    print('About to evaluate {} parameter sets.'.format(len(grid)))
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    final_scores = pool.map(evaluate_single, list(enumerate(grid)))

    print('Best parameter set was {} with score of {}'.format(grid[np.argmin(final_scores)], np.min(final_scores)))
    print('Worst parameter set was {} with score of {}'.format(grid[np.argmax(final_scores)], np.max(final_scores)))
    print('Execution time: {} sec'.format(time.time() - start_time))

if __name__ == '__main__':
    run()