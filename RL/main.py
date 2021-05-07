import json
import time 
from datetime import datetime
import matplotlib.pyplot as plt
import rl_env.rl_path_ev as env
import agent.agent as agents

# print()
# print(f'Main Path: {os.getcwd()}')

PATH = '../RL/agent/'

MODEL_PATH = '../models/Qtables/'

power_data = '../RL/Data/Avg_House_n/nonsolarhouse/22.npy'

img_folder_path = '../RL/imgs/' 

def plot_rl_env(network_env, save_plt_path = None):
    
    network_env.plot_nodes()
    plt.axis('off')
    axis = plt.gca()
    axis.set_xlim([1.4*x for x in axis.get_xlim()])
    axis.set_ylim([1.4*y for y in axis.get_ylim()])
    plt.tight_layout()
    if save_plt_path != None:
      #shouldn't be used for loonger than a month
      dt_string =  datetime.now().strftime("%d_%H_%M_%S_%f")
      plt.savefig(save_plt_path+dt_string+'.png')
    plt.pause(2)
    plt.close()

def main():
  "an example of how to use the env and agents together"
  #agent parameter can be change with json files
  with open(PATH+'nissan_leaf_2017.json') as f:
  # with open(PATH+'nissan_leaf_2019.json') as f:
  # with open(PATH+'dying_nissan_leaf.json') as f:
    nissan_leaf = json.load(f)


  #popular use ep run times, speed varies depending on hardware
  # but generally 1000 eps ~ 1-2 mins
  # ep = 1000
  # ep = 5000
  # ep = 50000
  ep = 2

  # ep // 10 saving every 1/10 qtable
  # sample = ep // 10

  #make sample out of range of ep (rec: >= 3*ep) to avoid saving data
  sample = 3*ep
  
  #example how init a agent, only requirement is the dict from the json
  car_agent = agents.SmartQLAgent(nissan_leaf, sample, quiet = False)
  # car_agent = agents.RandomDataAgent(nissan_leaf)

  #example how init a env, the agent(s)

  network_env = env.graph_env(agents= [car_agent], 
          nonsolarhouse_data_paths = [power_data])

  #begining reset 
  obs = network_env.reset()
  #init table
  car_agent.create_qtable()

  
  n = ep * 21
  tic = time.time()
  for i in range(n):
      #main loop 
      #uncomment to turn on visual with saving 
      # plot_rl_env(network_env, img_folder_path)
      #uncomment to turn on visual 
      plot_rl_env(network_env)
      
      #how to fet up loop for env - agent interaction 
      # marl doesn't function yet.  
      obs = network_env.step(*car_agent.step(obs[0]))
      
  toc = time.time()
  tictoc = toc - tic 
  print(f'This took {tictoc:.2f} secs')
  
if __name__ == "__main__":
  main()


