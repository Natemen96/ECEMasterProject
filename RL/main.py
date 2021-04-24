# from ECEMasterProject.RL.rl_env.rl_path_ev import graph_env
import json
import os 
import random 
import time 

import matplotlib.pyplot as plt

import rl_env.rl_path_ev as env
import agent.agent as agents

# print()
# print(f'Main Path: {os.getcwd()}')

PATH = '../Demo/ECEMasterProject/RL/agent/'

MODEL_PATH = '../Demo/ECEMasterProject/models/Qtables/'

power_data = 'ECEMasterProject/RL/Data/Avg_House_n/nonsolarhouse/22.npy'

def plot_rl_env(network_env):
    network_env.plot_nodes()
    plt.axis('off')
    axis = plt.gca()
    axis.set_xlim([1.4*x for x in axis.get_xlim()])
    axis.set_ylim([1.4*y for y in axis.get_ylim()])
    plt.tight_layout()
    plt.pause(2)
    plt.close()

if __name__ == "__main__":

  with open(PATH+'nissan_leaf_2017.json') as f:
  # with open(PATH+'nissan_leaf_2019.json') as f:
  # with open(PATH+'dying_nissan_leaf.json') as f:
    nissan_leaf = json.load(f)

    # car_agent = agents.RandomAgent(nissan_leaf)
  #1000 ~ 1 min
  # ep = 1000
  # ep = 5000
  ep = 50000
  # ep = 100
  #make sample out of range of ep (rec: >= 3*ep) to avoid saving data
  sample = ep // 10
  # sample = 3*ep
  car_agent = agents.SmartQLAgent(nissan_leaf, sample, quiet = False)
  # car_agent = agents.RandomDataAgent(nissan_leaf)

  network_env = env.graph_env(agents= [car_agent], 
          nonsolarhouse_data_paths = [power_data])
  obs = network_env.reset()
  #init table
  car_agent.create_qtable()

  
  n = ep * 21
  tic = time.time()
  for i in range(n):
      #uncomment to turn on visual
      # plot_rl_env(network_env)

      #random agent doesn't use obs

      # network_env.step(*car_agent.step())
      # print()
      
      #smart agent does use obs
      obs = network_env.step(*car_agent.step(obs[0]))
      
  toc = time.time()
  tictoc = toc - tic 
  print(f'This took {tictoc:.2f} secs')

