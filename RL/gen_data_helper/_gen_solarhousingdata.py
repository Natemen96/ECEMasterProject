import os
import numpy as np 
np.random.seed(7)

import matplotlib.pyplot as plt

from tslearn.clustering import TimeSeriesKMeans

filepath = '../Demo/ECEMasterProject/models/KM/KM1.h5'

km=TimeSeriesKMeans.from_hdf5(filepath)
n = 96
data = np.random.uniform(low = -6, high= 3, size=(n,1))

data_class = km.predict(data)
print(data_class)
# while 1 in data_class:
def update_data(data, data_class, check = 1):
    for i in range(len(data)):
        if data_class[i] == check:
            data[i] = np.random.uniform(low = -6, high= 3)
    return data

check = 0

while check in data_class:
    update_data(data, data_class, check)
    data_class = km.predict(data)

print(data_class)

plt.plot(data)
plt.tight_layout()
plt.grid(True)
plt.show()