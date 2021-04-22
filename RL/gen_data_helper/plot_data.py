import os
import numpy as np 
np.random.seed(7)
import matplotlib.pyplot as plt

file0 = r'ECEMasterProject\RL\Data\Avg_House_0\solarhouse\0.npy'
file1 = r'ECEMasterProject\RL\Data\Avg_House_1\solarhouse\0.npy'

data1 = np.load(file0)
data2 = np.load(file1)

plt.plot(data1)
plt.plot(data2)
plt.tight_layout()
plt.grid(True)
plt.show()