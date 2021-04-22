import os
import numpy as np
np.random.seed(7)

import matplotlib.pyplot as plt

mainfolder = 'ECEMasterProject\RL\Data'
dayeven = mainfolder+'\Avg_House_0'
dayodd = mainfolder+'\Avg_House_1'
daytotal = mainfolder+'\Avg_House_n'

def get_pathes(root_dir):
    file_set = []
    for dir_, _, files in os.walk(root_dir):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, root_dir)
            rel_file = os.path.join(rel_dir, file_name)
            file_set.append(rel_file)
    return file_set

evenlist = get_pathes(dayeven)

for rpath in evenlist:
    day0 = np.load(dayeven+'\\'+rpath)
    day1 = np.load(dayodd+'\\'+rpath)
    dayn = np.concatenate((day0,day1))
    # np.save(daytotal+'\\'+rpath, dayn, allow_pickle=False)
    plt.plot(dayn)
    plt.title(rpath)
    plt.pause(2)
    plt.close()
