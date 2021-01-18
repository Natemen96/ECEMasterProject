import numpy as np 
# import math
# import os 
# import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import multiprocessing
# import seaborn as sns
# import pickle
import pandas as pd
import time
# import datetime

# from sklearn import tree
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LinearRegression,  RANSACRegressor, TheilSenRegressor, Ridge 
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.svm import SVR
from sklearn.model_selection import cross_validate, train_test_split, cross_val_score, GridSearchCV, ParameterGrid
# from sklearn.multioutput import MultiOutputRegressor
# from sklearn.kernel_ridge import KernelRidge

from statsmodels.tsa.holtwinters import ExponentialSmoothing as HWES
# import statsmodels.api as sm
# from statsmodels.api import OLS

# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# from statsmodels.tsa.statespace.sarimax import SARIMAX

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

#HW 
df = pd.DataFrame(housing_data[0], columns=['15min_ints','grid']).set_index('15min_ints')
RANDOM_SEED = 42
train_df = df.iloc[:-900, :]
test_df = df.iloc[-900:, :]

pred_df = test_df.copy()

grid_params = {
    'seasonal_periods': np.linspace(2,300, num=299),
    'damped_trend': [True,False],
    'initialization_method': ['estimated','heuristic','legacy-heuristic']
}
grid = list(ParameterGrid(grid_params))

def evaluate_single(args):
    index, params = args
    print('Evaluating params: {}'.format(params))
    params = {**params}

    pred = HWES(train_df, trend="add", seasonal="add", **params).fit().forecast(900)
    score = np.sqrt(np.mean(np.square(test_df.values - pred.values)))

    print('Finished evaluating set {} with score of {}.'.format(index, score))
    return score

def run():
    start_time = time.time()
    print('About to evaluate {} parameter sets.'.format(len(grid)))
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()//2)
    final_scores = pool.map(evaluate_single, list(enumerate(grid)))

    print('Best parameter set was {} with score of {}'.format(grid[np.argmin(final_scores)], np.min(final_scores)))
    print('Worst parameter set was {} with score of {}'.format(grid[np.argmax(final_scores)], np.max(final_scores)))
    print('Execution time: {} sec'.format(time.time() - start_time))

if __name__ == '__main__':
    run()