import json
import os 
import random 

# sys.path.append('/ECEMasterProject/RL/rl_env')
# import rl_path_ev 
print()
print(f'Agent Path: {os.getcwd()}')

# PATH = '../Demo/ECEMasterProject/RL/agent/'
  # print(nissan_leaf)


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
    pass
    self.ev_loc = None
  def step(self, obs=None):
    #return an action, use obs to help 
    pass

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

    for act in self.env_edge_actions_cost.items():
      actions.append(act)
    return actions
    


  def do_action(self, action):
    "expect edges or current node"
    print(type(action))
    print(action)
    if type(action) == tuple:
      self.movement(action[1])
      return action
    else:
      getattr(self, action)(self.env_node_actions_cost[1])
      return "nothing"

  
  # def set_home_location(self, home_location):
  #   self.home_loc = home_location
  # def black_out_target(self, black_loc):
  #   self.black_loc = black_loc

  def set_ev_location(self, ev_location):
    self.ev_loc = ev_location

  def set_charging_locations(self, charging_locations):
    # charging_locations = list(filter(None, charging_locations))
    self.charging_locations = charging_locations

  def chargeup(self, cost = 0, flag = False):
    #check charge
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

  
  def movement(self, cost):
     self.unload(cost)

  def reset(self):
    self.chargeup(flag=True)

  def dead_battery_check(self):
    if self.current_battery < 0:
      self.dead_battery = True
    else:
      pass 
    # print(self.current_battery)

class RandomAgent(BasicAgent):
  def __init__(self, car):
    super().__init__(car)
    self.last_action = 'nothing'

  def step(self, obs=None):
    # super().step(obs)
    print()
    print('Agent Step')
    actions = self.get_available_actions()
    action = random.choice(actions)
    
    self.dead_battery_check()
    if self.dead_battery == True:
      return self.ev_loc, "nothing"
    
    self.last_action = self.do_action(action)
    return self.ev_loc, self.last_action


if __name__ == "__main__":
  with open(PATH+'nissan_leaf_2017.json') as f:
    nissan_leaf = json.load(f)
    # print(nissan_leaf)
    # car_agent = BasicAgent(nissan_leaf)
    car_agent = RandomAgent(nissan_leaf)
    # print(car_agent.avg_energy_com, car_agent.battery)
    car_agent.reset()
    # print(car_agent.current_battery)
  pass