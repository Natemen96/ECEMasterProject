import os 
import random 
import csv
# from algos.QL import QLearningTable
from agent.algos.QL import QLearningTable
import math
from datetime import datetime

print()
print(f'Agent Path: {os.getcwd()}')

dt_string =  datetime.now().strftime("%m_%d_%H_%M")
MODEL_PATH = f'../models/Qtables/{dt_string}/'
DATA_PATH = f'../RL/agent/Sim_Data/reward_{dt_string}.csv'
class BasicAgent():
  def __init__(self,car):
    """[BasicAgent: Basic Agent that act as skeleton for other agent. Won't work by it's self.]

    Args:
        car ([dict]): [car information in the form of a python dictionary]
    """    
    self.model = car['model']
    self.make = car['make']
    self.year = car['year']
    self.avg_energy_com = float(car['avg_energy_consumption(kWh/mile)'])
    self.MAX_BATTERY = float(car['battery_capacity(kWh)'])
    self.current_battery = float(car['battery_capacity(kWh)']) #assuming tank is full at start
    self.dead_battery = False 
    print(f'Data Load Successfully for {self.make} - {self.model} - {self.year}')
    # print(self.current_battery)
    # print(self.MAX_BATTERY)
    self.basic_actions = ("chargeup","unload")
    self.ev_loc = None
    self.ep = -1

  def step(self, obs=None):
    """[step, where the agent decides it's next action]

    Args:
        obs ([obs object], optional): [obs object from env]. Defaults to None.
    """    
    #return an action, use obs to help 
    pass

  def set_all_loc(self,nodes):
    """[get all possible locations]

    Args:
        nodes ([type]): [description]
    """    
    self.all_loc = nodes

  def get_qtable_actions(self):
    """[set all possible actions for qtable, actions function and available nodes]

    Returns:
        [list]: [all possible actions for qtable]
    """    
    qtable_actions = ['nothing']
    for act in self.basic_actions:
      qtable_actions.append(act)
    for node in self.all_loc:
      qtable_actions.append(node)
    return qtable_actions

  def set_available_actions(self,env_actions):
    """[get actions from env, gets more organized in getter]

    Args:
        env_actions ([type]): [description]
    """    
    self.env_edge_actions_cost = env_actions
    # print(env_actions)
    self.env_node_actions_cost = env_actions.popitem()
    #  = env_actions
    # print(self.env_edge_actions_cost)
    # print(self.env_node_actions_cost)
  

  def get_available_actions(self):
    """[get actions form env]

    Returns:
        [list]: [available actions ]
    """    
    actions = []
    for act in self.basic_actions:
      actions.append(act)
    # self.qtable_actions = actions
    for act in self.env_edge_actions_cost.items():
      actions.append(act)
    return actions
    


  def do_action(self, action):
    """[takes action and performs it]

    Args:
        action ([str or tuple]): [if str, call action's function otherwise do movement on map]

    Returns:
        [type]: [description]
    """   
    # print(type(action))
    # print(action)
    if type(action) == tuple:
      self.movement(action[1])
      return action
    else:
      #pass node cost if there is any
      getattr(self, action)(self.env_node_actions_cost[1])
      return action

  
  # def set_home_location(self, home_location):
  #   self.home_loc = home_location
  def set_black_out_targets(self, black_loc):
    """[set black out targets locations (blackout w/o solar power) for agent logic]

    Args:
        black_loc ([type]): [black node locations]
    """    
    self.black_loc = black_loc

  def set_ev_location(self, ev_location):
    """[set current ev location for agent's logic]

    Args:
        ev_location ([type]): [en location]
    """    
    self.ev_loc = ev_location

  def set_charging_locations(self, charging_locations):
    """[set possible charging locations (charging stations and home) for agent logic]

    Args:
        charging_locations ([type]): [charging locations locations]
    """    
    self.charging_locations = charging_locations

  def chargeup(self, cost = 0, flag = False):
    """[action that allows the agent to restore it's power]

    Args:
        cost (float): [not use for method flexibly with other action methods]
        flag (bool, optional): [For game reset, flag will restore power]. Defaults to False.
    """    
    #check charge 
    # print('old charge')
    if (self.ev_loc in self.charging_locations) or flag:
      self.current_battery = float(self.MAX_BATTERY)
    else:
      pass

  def unload(self,cost):
    """[take power from car]

    Args:
        cost ([float]): [power that being drawn]
    """    
    # print(self.current_battery)
    # if (self.ev_loc in self.black_loc):
    #   self.current_battery -= cost 
    # else:
    self.current_battery -= cost
    # print(self.current_battery)

  def nothing(self, cost):
    """[do nothing buffer]

    Args:
        cost ([float]): [cost is passed for flexibility with other actions]
    """    
    pass 

  def movement(self, cost):
    """[calculate cost of movement when agent crosses edge]

    Args:
        cost ([float]): [miles length of edge]
    """    
    "assuming cost is in miles"
    cost = self.avg_energy_com*cost
    self.unload(cost)

  def reset(self):
    """[reset agent to prepare for next ep]
    """    
    self.dead_battery = False 
    self.chargeup(flag=True)
    self.ep +=1
    self.last_action = None
    self.previous_state = None
    print(f'Current ep {self.ep}')

  def dead_battery_check(self):
    """[dead battery flag setter, check if current battery is less than 0]
    """    
    if self.current_battery < 0:
      self.dead_battery = True
  
  def unload_tracker_init(self):
    """[keep track of what nodes are being unload so reward will go down for non-diversity]
    """
    unload_tracker = []
    for i in range(len(self.all_loc)):
      unload_tracker.append(0)
    self.unload_tracker = unload_tracker

  def unload_tracker_update(self, node):
    """[get unload node and add a increase counter]

    Args:
        node ([int]): [node identifier]
    """    
    self.unload_tracker[node] += 1
    # print(self.current_battery)

class _RandomAgent(BasicAgent):
  "deprecated, but kept for historical reasons"
  def __init__(self, car):
    super().__init__(car)
    self.last_action = 'nothing'

  def step(self, obs=None):
    """[step, where the agent decides it's next action]

    Args:
        obs ([obs object], optional): [obs object from env]. Defaults to None.

    Returns:
        [type]: [current agent location and it's next action]
    """    
    # print()
    # print('Agent Step')
    actions = self.get_available_actions()
    action = random.choice(actions)
        
    self.last_action = self.do_action(action)
    self.dead_battery_check()
    if self.dead_battery == True:
      self.last_action = 'nothing'
      # return self.ev_loc, "nothing"
    return self.ev_loc, self.last_action
  
  # def reset(self):
  #   super().reset()


class SmartQLAgent(BasicAgent):
  def __init__(self, car, sample_rate = 100, qtabletraining = True, quiet = True ):
    """[SmartQLAgent: Smart Agent that uses Qtable to make decisions]

    Args:
        car ([dict]): [car information in the form of a python dictionary]
        sample_rate (int, optional): [decides how often a sample of the qtable is taken. If left to default it's every 1/100 of total ep]. Defaults to 100.
        qtabletraining (bool, optional): [Flag for turning qtable training on]. Defaults to True.
        quiet (bool, optional): [Flag for turning data collection on]. Defaults to True.
    """    
    super().__init__(car)
    self.last_action = None
    self.previous_state = None
    self.i = 0
    self.sample_rate = sample_rate
    self.qtabletraining = qtabletraining
    self.quiet = quiet

  def step(self, obs):
    """[step, where the agent decides it's next action. Smart Agent uses Qtable to make decsions]

    Args:
        obs ([obs object]): [obs object from env]

    Returns:
        [type]: [current agent location and it's next action]
    """    
    self.i += 1
    self.obs = obs

    # super().step(obs)
    # print()
    # print('Agent Step')
    state = str(tuple(list(self.obs.get_obs())+[round(self.current_battery,0)])) 
    actions = self.get_available_actions()
    
    self.action = self.qtable.choose_action(state,self.ep)
    if self.action not in (actions + ['nothing']):
        self.action = int(self.action)
    elif self.action == 'unload':
      self.unload_tracker_update(self.ev_loc)
    # action = random.choice(actions)
    def select_action(action, actions_list):
      if action in actions_list:
        return action
      elif action == actions_list[-1][0][0]:
        return 'nothing'
      else:
        for i in range(2,len(actions_list)):
          if actions_list[i][0][1] == action:
            return actions_list[i] 
        return 'nothing'

    action_comd = select_action(self.action, actions)
    action_comd = self.do_action(action_comd)
    self.dead_battery_check()
    if self.dead_battery == True:
      action_comd = 'nothing'
      self.action = 'nothing'
    if (self.last_action is not None) and (self.qtabletraining==True):
        self.qtable.learn(self.previous_state,
                        self.last_action,
                        self.obs.get_reward(), #need this
                        'last' if self.obs.get_last() else state)

    self.last_action = self.action
    self.previous_state = state
      # return self.ev_loc, "nothing"
    return self.ev_loc, action_comd

  def dead_battery_check(self):
    """[dead battery check, agent reward is set to zero for dead battery ]
    """    
    if self.current_battery < 0:
      self.dead_battery = True
      self.obs.set_reward(-1)

  def chargeup(self, cost = 0, flag = False):
    """[chargeup gives agent reward based on how low it's battery was. Reward = (Battery_0  - Battery_i)/Battery_0 ]

    Args:
        cost (int, optional): [not use for method flexibly with other action methods]. Defaults to 0.
        flag (bool, optional): [For game reset, flag will restore power ]. Defaults to False.
    """    
    #check charge , make sure this working
    # print('new charge')
    if flag:
      self.current_battery = float(self.MAX_BATTERY)
    
    elif (self.ev_loc in self.charging_locations):
      if self.current_battery != float(self.MAX_BATTERY):
        reward = (float(self.MAX_BATTERY) - (self.current_battery)**(1))/float(self.MAX_BATTERY)
        reward = max(reward,0)
        self.obs.add_reward(reward)
      self.current_battery = float(self.MAX_BATTERY)

    else:
      pass

  def unload(self,cost):
    """[unload give agent reward based on how often it was done it before that node. reward can't go below 0. function: reward = ((-log_10((# of unloads for node + 30)/10) + .53) * cost_of_unload)*25]

    Args:
        cost ([type]): [description]
    """    
    if (self.ev_loc in self.black_loc) and self.action == 'unload':
      unload_tic = self.unload_tracker[self.ev_loc]
      reward = ((-1*math.log10((unload_tic + 30)/10)+.53) * cost)*25
      reward = max(reward,0)
      self.obs.add_reward(reward)
    self.current_battery -= cost
    # print(self.current_battery)

  def reset(self):
    """[reset agent to prepare for next ep]
    """    
    self.dead_battery = False 
    self.chargeup(flag=True)
    self.last_action = None
    self.previous_state = None
    self.unload_tracker_init()
    if (self.ep % self.sample_rate == 0) and (self.ep > 0) and (self.qtabletraining == True):
      if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
      self.qtable.save_qtable(self.ep, MODEL_PATH)
    if self.quiet != True and self.ep > 0:
      write_to_csv(self.obs.get_reward(), DATA_PATH)
    self.ep +=1
    self.i = 0
    print(f'Current ep {self.ep}')
  
  def create_qtable(self):
    """[initialize qtable from qtable class]
    """    
    self.qtable = QLearningTable(self.get_qtable_actions())

  def load_qtable(self, qtable_file):
    """[load qtable from h5 file]

    Args:
        qtable_file ([str]): [h5 file where qtable (panda dataframe) was stored]
    """    
    self.qtable = QLearningTable(self.get_qtable_actions())
    self.qtable.load_qtable(qtable_file)

def write_to_csv(tosave, PATH):
  """[Helper function to write to csv to make data collection less painful]

  Args:
      tosave ([type]): [data to be save, gets converted to list]
      PATH ([type]): [path to save the data to]
  """  
  if not os.path.exists(PATH):
      with open(PATH, 'w', newline='') as csvfile:
          csvfile.close()
  with open(PATH, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow([tosave])


class RandomDataAgent(SmartQLAgent):
  def __init__(self, car):
    """[RandomDataAgent: Used for data collection of random agent. Doesn't use Observation.]

    Args:
        car ([dict]): [car information in the form of a python dictionary]
    """    
    super().__init__(car, qtabletraining = False, quiet = False)

  def step(self, obs=None):
    """[step, where the agent decides it's next action. Random Agent makes a random choice.]

    Args:
        obs ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """    
    # print()
    # print('Agent Step')
    self.i += 1
    self.obs = obs

    actions = self.get_available_actions()
    self.action = random.choice(actions)
    if self.action not in (actions + ['nothing']):
        self.action = int(self.action)
    elif self.action == 'unload':
      self.unload_tracker_update(self.ev_loc)

    def select_action(action, actions_list):
      if action in actions_list:
        return action
      elif action == actions_list[-1][0][0]:
        return 'nothing'
      else:
        for i in range(2,len(actions_list)):
          if actions_list[i][0][1] == action:
            return actions_list[i] 
        return 'nothing'
        
    action_comd = select_action(self.action, actions)
    action_comd = self.do_action(action_comd)
    self.dead_battery_check()
    if self.dead_battery == True:
      action_comd = 'nothing'
      self.last_action = 'nothing'
      # return self.ev_loc, "nothing"
    self.last_action = self.action

    return self.ev_loc, action_comd
  
  def reset(self):
    """[Uses Smart Agent reset]
    """    
    super().reset()

if __name__ == "__main__":

  pass