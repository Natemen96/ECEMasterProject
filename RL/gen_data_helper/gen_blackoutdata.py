# %%
import numpy as np 
np.random.seed(7)
import matplotlib.pyplot as plt
import os 
print(os.getcwd())
PATH = "../Demo/ECEMasterProject/RL/Data/"
import pandas as pd


# # Data Preprocessing
# %%
Dataset = r'../Demo/ECEMasterProject/scripts/Data/TexasBlackout.csv'
fulldata = pd.read_csv(Dataset, thousands=',') 
fulldata['Outage %'] = fulldata['Outage %'].str.rstrip('%').astype('float') / 100.0


# %%
sorteddata=fulldata.sort_values(by = ['ID', 'DateTime'])
ids=sorteddata['ID'].unique().tolist()


# %%
blackout_data = []

for i in range(len(ids)):
    blackout_data.append(sorteddata.loc[sorteddata.ID==ids[i]])    
    blackout_data[i] = blackout_data[i].reset_index().drop(columns=['index'])


# %%
#get min / max idx and size
max_size = 0
max_i = 0
min_size = np.inf
min_i = 0
for i in range(len(ids)):
    size=len(blackout_data[i])
    if size > max_size:
        max_i = i
        max_size = size 
    if size < min_size:
        min_i = i
        min_size = size
print(f'max_i: {max_i}, max_size: {max_size}')
print(f'min_i: {min_i}, min_size: {min_size}')

# %%
#get largest outrages 
large_outrage_list =[]
large_outrage_i_list = []
threshold = .70

for i in range(len(ids)):
    highoutage=max(blackout_data[i]['Outage %'])
    if highoutage > threshold:
        large_outrage_list.append(highoutage)
        large_outrage_i_list.append(i)
# print(large_outrage_list)
# print(len(large_outrage_list))


# %%
def moving_avg(x, w = 50):
    return np.convolve(x,np.ones(w),'valid')/w 


# %%
def remove_n(A,n=.1):
    "filter out very small numbers"
    return A[A > n]

# %%
plt.figure(figsize=(13, 8))
for i, j in enumerate(large_outrage_i_list):
    plt.subplot(4,4,i+1) 
    data = remove_n(moving_avg(blackout_data[j]['Outage %']))
    filename = f'{blackout_data[j]["County"][0]}'.replace(" ", "_")
    
    plt.plot(data, color = f'C{i}')
    plt.title(f'{filename}')
    plt.grid(True)
    np.save(PATH+f'{filename}', data, allow_pickle=False)
    
plt.tight_layout()
# plt.show()
