import os 
import random 
# from algos.QL import QLearningTable
from agent.algos.QL import QLearningTable
import math
from datetime import datetime
# sys.path.append('/ECEMasterProject/RL/rl_env')
# import rl_path_ev 
print()
print(f'Agent Path: {os.getcwd()}')

# PATH = '../Demo/ECEMasterProject/RL/agent/'
  # print(nissan_leaf)

dt_string =  datetime.now().strftime("%m_%d_%H_%M")
MODEL_PATH = f'../Demo/ECEMasterProject/models/Qtables/{dt_string}/'

class BasicAgent():
  def __init__(self,car):
    
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
    #return an action, use obs to help 
    pass

  def set_all_loc(self,nodes):
    self.all_loc = nodes

  def get_qtable_actions(self):
    qtable_actions = ['nothing']
    for act in self.basic_actions:
      qtable_actions.append(act)
    for node in self.all_loc:
      qtable_actions.append(node)
    return qtable_actions

  def set_available_actions(self,env_actions):
    self.env_edge_actions_cost = env_actions
    # print(env_actions)
    self.env_node_actions_cost = env_actions.popitem()
    #  = env_actions
    # print(self.env_edge_actions_cost)
    # print(self.env_node_actions_cost)
  

  def get_available_actions(self):
    actions = []
    for act in self.basic_actions:
      actions.append(act)
    # self.qtable_actions = actions
    for act in self.env_edge_actions_cost.items():
      actions.append(act)
    return actions
    


  def do_action(self, action):
    "expect edges or current node"
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
    self.black_loc = black_loc

  def set_ev_location(self, ev_location):
    self.ev_loc = ev_location

  def set_charging_locations(self, charging_locations):
    # charging_locations = list(filter(None, charging_locations))
    self.charging_locations = charging_locations

  def chargeup(self, cost = 0, flag = False):
    #check charge 
    # print('old charge')
    if (self.ev_loc in self.charging_locations) or flag:
      self.current_battery = float(self.MAX_BATTERY)
    else:
      pass

  def unload(self,cost):
    # print(self.current_battery)
    # if (self.ev_loc in self.black_loc):
    #   self.current_battery -= cost 
    # else:
    self.current_battery -= cost
    # print(self.current_battery)

  def nothing(self, cost):
    pass 

  def movement(self, cost):
    "assuming cost is in miles"
    cost = self.avg_energy_com*cost
    self.unload(cost)

  def reset(self):
    self.dead_battery = False 
    self.chargeup(flag=True)
    self.ep +=1
    self.last_action = None
    self.previous_state = None
    print(f'Current ep {self.ep}')

  def dead_battery_check(self):
    if self.current_battery < 0:
      self.dead_battery = True
  
  def unload_tracker_init(self):
    unload_tracker = []
    for i in range(len(self.all_loc)):
      unload_tracker.append(0)
    self.unload_tracker = unload_tracker

  def unload_tracker_update(self, node):
    self.unload_tracker[node] += 1
    # print(self.current_battery)

class RandomAgent(BasicAgent):
  def __init__(self, car):
    super().__init__(car)
    self.last_action = 'nothing'

  def step(self, obs=None):
    # super().step(obs)
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

class SmartQLAgent(BasicAgent):
  def __init__(self, car):
    super().__init__(car)
    self.last_action = None
    self.previous_state = None

  def step(self, obs):
    self.obs = obs
    # super().step(obs)
    # print()
    # print('Agent Step')
    state = str(tuple(list(self.obs.get_obs())+[round(self.current_battery,1)])) 
    actions = self.get_available_actions()
    
    action = self.qtable.choose_action(state,self.ep)
    if action not in (actions + ['nothing']):
        action = int(action)
    elif action == 'unload':
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

    action_comd = select_action(action, actions)
    action_comd = self.do_action(action_comd)
    self.dead_battery_check()
    if self.dead_battery == True:
      action_comd = 'nothing'
      action = 'nothing'
    if self.last_action is not None:
        self.qtable.learn(self.previous_state,
                        self.last_action,
                        self.obs.get_reward(), #need this
                        'last' if self.obs.get_last() else state)

    self.last_action = action
    self.previous_state = state
      # return self.ev_loc, "nothing"
    return self.ev_loc, action_comd

  def dead_battery_check(self):
    if self.current_battery < 0:
      self.dead_battery = True
      self.obs.set_reward(-1)

  def chargeup(self, cost = 0, flag = False):
    #check charge , make sure this working
    # print('new charge')
    if flag:
      self.current_battery = float(self.MAX_BATTERY)
    
    elif (self.ev_loc in self.charging_locations):
      if self.current_battery != float(self.MAX_BATTERY):
        reward = (float(self.MAX_BATTERY) - self.current_battery)/float(self.MAX_BATTERY)
        self.obs.add_reward(reward)
      self.current_battery = float(self.MAX_BATTERY)

    else:
      pass

  def unload(self,cost):
    # print(self.current_battery)
    # print('new unload')
    if (self.ev_loc in self.black_loc):
      unload_tic = self.unload_tracker[self.ev_loc]
      reward = math.log10((unload_tic + 30)/10) * cost
      self.obs.add_reward(reward)
    self.current_battery -= cost
    # print(self.current_battery)

  def reset(self):
    self.dead_battery = False 
    self.chargeup(flag=True)
    self.last_action = None
    self.previous_state = None
    self.unload_tracker_init()
    if (self.ep % 10 == 0) and (self.ep > 0):
      if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
      self.qtable.save_qtable(self.ep, MODEL_PATH)
    self.ep +=1
    print(f'Current ep {self.ep}')
  
  def create_qtable(self):
    self.qtable = QLearningTable(self.get_qtable_actions())


if __name__ == "__main__":
  # with open(PATH+'nissan_leaf_2017.json') as f:
  #   nissan_leaf = json.load(f)
  #   # print(nissan_leaf)
  #   # car_agent = BasicAgent(nissan_leaf)
  #   car_agent = RandomAgent(nissan_leaf)
  #   # print(car_agent.avg_energy_com, car_agent.battery)
  #   car_agent.reset()
  #   # print(car_agent.current_battery)
  pass