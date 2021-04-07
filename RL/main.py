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

def run_loop(agents, env, max_episodes=0):
  """A run loop to have agents and an environment interact."""
  total_frames = 0
  total_episodes = 0
  start_time = time.time()

  try:
    while not max_episodes or total_episodes < max_episodes:
      total_episodes += 1
      obs = env.reset() #TODO: make obs class, make it per agent
      for a in agents:
        a.reset()
      while True:
        total_frames += 1
        actions = [agent.step(obs)
                   for agent, obs in zip(agents, obs)]
        if obs[0].last(): #TODO: obs class neeed this
          break
        obs = env.step(actions)
  except KeyboardInterrupt:
    pass
  finally:
    elapsed_time = time.time() - start_time
    print("Took %.3f seconds for %s steps: %.3f fps" % (
        elapsed_time, total_frames, total_frames / elapsed_time))


if __name__ == "__main__":

  with open(PATH+'nissan_leaf_2017.json') as f:
#   with open(PATH+'nissan_leaf_2019.json') as f:
  # with open(PATH+'dying_nissan_leaf.json') as f:
    nissan_leaf = json.load(f)

    # car_agent = agents.RandomAgent(nissan_leaf)
    car_agent = agents.SmartQLAgent(nissan_leaf)

    network_env = env.graph_env(agents= [car_agent])
    obs = network_env.reset()
    #init table
    car_agent.create_qtable()
    n = 1000
    for i in range(n):
        #uncomment to turn on visual, TODO: (Low) Make into function?
        # network_env.plot_nodes()
        # plt.pause(4)
        # plt.close()
        # network_env.step(*car_agent.step())
        # print()
        # print(obs)
        obs = network_env.step(*car_agent.step(obs[0]))
        # print(obs)

    car_agent.qtable.save_qtable(n, MODEL_PATH)
