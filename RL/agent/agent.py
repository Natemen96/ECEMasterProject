import json
import os 
import random 

# sys.path.append('/ECEMasterProject/RL/rl_env')
# import rl_path_ev 
print()
print(f'Agent Path: {os.getcwd()}')

PATH = '../Demo/ECEMasterProject/RL/agent/'
  # print(nissan_leaf)


class BasicAgent():
  def __init__(self,car):
    
    self.model = car['model']
    self.make = car['make']
    self.year = car['year']
    self.avg_energy_com = float(car['avg_energy_consumption(kWh/mile)'])
    self.MAX_BATTERY = float(car['battery_capacity(kWh)'])
    self.current_battery = float(car['battery_capacity(kWh)']) #assuming tank is full at start
    print(f'Data Load Successfully for {self.make} - {self.model} - {self.year}')
    # print(self.current_battery)
    # print(self.MAX_BATTERY)
    self.basic_actions = ("chargeup","unload")
    pass
  
  def step(self, obs=None):
    #return an action, use obs to help 
    pass

  def set_available_actions(self,env_actions):
    self.env_edge_actions_cost = env_actions
    # print(env_actions)
    self.env_node_actions_cost = env_actions.popitem()
    #  = env_actions
    print(self.env_edge_actions_cost)
    print(self.env_node_actions_cost)


  

  def get_available_actions(self):
    actions = []
    for act in self.basic_actions:
      actions.append(act)

    for act in self.env_edge_actions_cost.items():
      actions.append(act)
    return actions
    


  def do_action(self, action):
    "expect edges or current node"
    if type(action) == type(tuple):
      self.movement(self.env_actions[action])
      return action
    else:
      getattr(self, action)(self.env_node_actions_cost[1])
      return None

  
  # def set_home_location(self, home_location):
  #   self.home_loc = home_location

  def set_ev_location(self, ev_location):
    self.ev_loc = ev_location

  def set_charging_locations(self, charging_locations):
    self.charging_locations = charging_locations

  def chargeup(self, cost = 0):
    #check charge
    if self.ev_loc in self.charging_locations:
      self.current_battery = float(self.MAX_BATTERY)
    else:
      pass

  def unload(self,cost):
    self.current_battery -= cost
    pass 
  
  def movement(self, cost):
     self.unload(cost)

  def reset(self):
    self.chargeup()
    # print(self.current_battery)

class RandomAgent(BasicAgent):
  def __init__(self, car):
    super().__init__(car)

  def step(self, env_actions,obs=None):
    # super().step(obs)
    actions = self.get_available_actions(env_actions)
    action = random.choice(actions)
    self.do_action(action)
    # return action


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