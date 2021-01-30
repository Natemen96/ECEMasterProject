import cv2
import numpy as np 
import os 
import matplotlib.pyplot as plt
import seaborn as sns 
import pickle
import pandas as pd
import time
sns.set_theme()

def main():
    Dataset = r'15minute_data_newyork\15minute_data_newyork.csv'
    t1 = time.time()
    data = pd.read_csv(Dataset) 
    t2 = time.time()

    print(t2-t1)
    # savedata = r'SaveData\\'
    # Answers = r'Hw_Results\\'

if __name__ == "__main__":
    main()