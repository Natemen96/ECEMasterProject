import sys 
import os
# print(f'Env Path: {os.getcwd()}')

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from itertools import combinations, groupby
import copy 

# PATH = '../Data/'
PATH = '../Demo/ECEMasterProject/RL/Data/'

def blen(lst):
    "Better len for list, doesn't count Nones"
    return sum(x is not None for x in lst)

class Observation():
    def __init__(self):
        self.obs = None 
        self.reward = 0 
        self.last = False
        
    def set_obs(self, obs):
        self.obs = obs 
        
    def get_obs(self):
        return self.obs 
    
    def add_reward(self,reward):
        self.reward += reward

    def set_reward(self, reward):
        self.reward = reward 
        
    def get_reward(self):
        return self.reward

    def set_last(self,last_flag):
        self.last = last_flag
        
    def get_last(self):
        return self.last 


class graph_env():
    def __init__(self, n = 5, numofhome = 1, numofblackout = 1, numofblackoutws = 0, numofchargingstation = 0, max_actions = 3, blackout_str = 'Brazoria', agents = [None]):
        """Takes in a randomly generated graph, and keeps track of ep infomation
        numofhome - number of homes for agent starting point: int
        numofblackout - number of houses with blackout: int
        numofblackout - number of houses with solarpower: int
        blackout_str - Reads Blackout data from npy file: str
        """
        self.kwags = (n, numofhome, numofblackout, numofblackoutws, numofchargingstation,max_actions,blackout_str, agents)
        self.game_over = False
        self.game_over_reasons = ['All Agents Stuck', 'Power Back', "Week's Over"]
        self.game_over_reason = None
        assert numofhome == len(agents), "Env Load Error: Number of homes must be equal number of agents"
        # self.ev = ev
        # self.day = 0
        self.agents = agents 
        # print(agents)
        self.len_agents = blen(agents)
        
        # self.ep = 0
        self.i = 0
        # self.timestep = 0
        self.max_days = 7
        
        # self.actionsdone = 0
        
        self.max_actions = 1 if ((max_actions -1) < -1)  else  max_actions
        self.max_i = self.max_days * self.max_actions
        # self.max_actions = 1 if ((max_actions -1) < -1)  else  max_actions #action limit can't be less than 0
        # self.graph = G
        self.graph = self.gnp_random_connected_graph(n=n)

        self.color_map = []
        self.size_map = []

        #get all init graph information 
        self.allnodes = list(self.graph.nodes())
        self.node_status = dict.fromkeys(self.allnodes,0)
        

        self.home_nodes, buffer_nodes = self.init_update_graph(self.allnodes, numofhome,5)
        self.blackws_nodes, buffer_nodes = self.init_update_graph(buffer_nodes, numofblackoutws,2)
        self.black_nodes, buffer_nodes = self.init_update_graph(buffer_nodes, numofblackout,1)
        self.charging_nodes, self.buffer_nodes = self.init_update_graph(buffer_nodes, numofchargingstation,4)
        # print(self.black_nodes)
        #set costs
        self.set_cost(n)
        #EVs start at home
        self.EV_locations = copy.deepcopy(self.home_nodes)
        # print(self.home_nodes,self.charging_nodes)
        #give agents info
        self.get_available_action()
        self.agents_obs = []
        for i,agent in enumerate(self.agents):
            if self.charging_nodes == [None]:
                agent.set_charging_locations(self.home_nodes)
            else:
                agent.set_charging_locations(self.home_nodes + self.charging_nodes)
            agent.set_ev_location(self.EV_locations[i])
            agent.set_black_out_targets(self.blackws_nodes + self.black_nodes)
            agent.set_available_actions(self.actions[i])
            agent.set_all_loc(self.allnodes)
            # agent.set_qtable_actions()
            obs = Observation()
            self.agents_obs.append(obs)
            agent.reset()

        #delete None dict 
        try:
            del self.node_status[None]
        except KeyError: 
            pass
        #load blackout data
        try:
            blackout_data = np.load(PATH+blackout_str+'.npy') 
        except OSError: 
            print (f'Could not open/read file: {PATH+blackout_str+".npy"}')
        self.get_power_samples(blackout_data, self.max_i)
        
        # for i,obs in enumerate(self.agents_obs):
        #     #update obs
        #     obs.set_obs(tuple(self.get_obs(self.EV_locations[i])))
        #     if obs.get_last():
        #         obs.set_last(False)

        print('Env loaded correctly, Simulation started')
    
    def step(self, ev_loc = None ,action = None):
        if self.game_over == True:
            return self.env_close() 
        # print()
        # print('Env Step')
        # print(ev_loc)
        # print(action)
        len_max_buffer = blen(self.buffer_nodes)+blen(self.blackws_nodes)+blen(self.black_nodes)
        # print(len_max_buffer)
        if self.i == self.max_i:
            self.game_over_reason = self.game_over_reasons[2]
            return self.env_close()
            
        elif blen(self.buffer_nodes) == len_max_buffer:
            self.game_over_reason = self.game_over_reasons[1]
            return self.env_close()
            
        else: 
            #TODO: Reduce this to a function?
            stuck_agents = []

            for i,agent in enumerate(self.agents):
                #give them to agents
                agent.set_available_actions(self.actions[i])

            self.update_ev_location(ev_loc,action)
            for i,agent in enumerate(self.agents):
                if agent.dead_battery == False:
                    #set location for EV
                    agent.set_ev_location(self.EV_locations[i])
                else:
                    stuck_agents.append(agent)

            if blen(stuck_agents) == self.len_agents:
                self.game_over_reason = self.game_over_reasons[0]
                return self.env_close()

            #get current actions for new locations
            self.get_available_action()

            for i,agent in enumerate(self.agents):
                #give them to agents
                agent.set_available_actions(self.actions[i])

            self.power_check() 

            self.i +=1 

            for i,obs in enumerate(self.agents_obs):
                #update obs
                obs.set_obs(tuple(self.get_obs(self.EV_locations[i])))
                if obs.get_last():
                    obs.set_last(False)
            return self.agents_obs

    

    def get_obs(self, node):
        obs = []
        len_path = dict(nx.all_pairs_dijkstra(self.graph,weight='cost'))
        for key, val in self.node_status.items():
            #get vals which hold status of each nodes 
            obs.append(val)
            #get cost to node from agent_loc 
            obs.append(round( len_path[node][0][key],1))
        obs.append(tuple(self.graph.edges(node)))
        return obs
            
    def reset(self):
        return self.env_close()
    
    def env_close(self):
        print(f'Game over: {self.game_over_reason}, please reinit')
        print(f'Game ended in {self.i} out of {self.max_i} steps')
        self.i = 0
        self.game_over = True
        self.__init__(*self.kwags)

        for i,obs in enumerate(self.agents_obs):
            #update obs
            obs.set_obs(tuple(self.get_obs(self.EV_locations[i])))
            obs.set_last(True)

        return self.agents_obs
        # return obs
        # for i,agent in enumerate(self.agents):
    

    def get_available_action(self):

        def list_to_dict(a):
            it = iter(a)
            res_dct = dict(zip(it, it))
            return res_dct

        actions = [] # a list of all actions per agent
        for ev in self.EV_locations:
            act_weights = []
            edges = list(self.graph.edges(ev))
            for e in edges:
                act_weights.append(e)
                weight = self.graph[e[0]][e[1]]["cost"] 
                act_weights.append(weight)
                # edge.append()
            # print(edges) 
            #add the node for node actions
            act_weights.append(ev)
            node_weight= self.graph.nodes[ev]["cost"]
            act_weights.append(node_weight)

            actions.append(list_to_dict(act_weights)) 
        self.actions = actions
        # pass

    def reward_output(self):
        "TODO: figure out reward for actions / obs"
        pass

    def ev_for_agents(self):
        return self.EV_locations 

    def init_update_graph(self,nodes,num_to_update,val):
        nodes_to_updates, buffer_nodes = self.remove_node(nodes, num_to_update)
        for node in nodes_to_updates:
            # print(home)
            node_update = {node: val}
            self.node_status.update(node_update)
        return nodes_to_updates, buffer_nodes

    def remove_node(self,nodes, numtoremove=1):
        if numtoremove < 1:
            return [None], nodes
        nodes = list(nodes)
        samples = random.sample(nodes, 1)
        new_nodes = list(set(nodes).symmetric_difference(set(samples)))
        return samples, new_nodes

    def set_cost(self,n):
        #TODO: reads from model not random 
        a = np.round(np.random.rand(n,n)[np.triu_indices(n)],1)
        
        for i,e in enumerate(self.graph.edges()):
            self.graph[e[0]][e[1]]["cost"] = a[i]

        for node in self.black_nodes:
            if node != None:
                self.graph.nodes[node]["cost"] = 30 
                # print(node)
        
        for node in self.blackws_nodes:
            if node != None:
                self.graph.nodes[node]["cost"] = 20

        for node in  self.home_nodes + self.charging_nodes + self.buffer_nodes:
            if node != None:
                self.graph.nodes[node]["cost"] = 0


    def get_power_samples(self, blackout_data, numofsample):
        self.blackout_samples = []
        totalsamples = len(blackout_data)
        for i in range(numofsample): 
            idx = int((i/numofsample)*totalsamples)
            self.blackout_samples.append(blackout_data[idx])

    def power_check(self):
        "read from blackout sample to figure out if power is back 1,2 -> 3 "

        p = self.blackout_samples[self.i]
        
        for node in self.black_nodes:
            if node == None:
                pass
            elif random.random() /2 < p:
                pass
            else: 
                #put power back on
                node_update = {node: 3}
                print(f'Power restored to node {node}')
                self.node_status.update(node_update)
                self.black_nodes.remove(node)
                self.buffer_nodes.append(node)

        for node in self.blackws_nodes:
            if node == None:
                pass
            elif random.random() /2 < p:
                pass
            else: 
                #put power back on
                node_update = {node: 3}
                print(f'Power restored to node {node}')
                self.node_status.update(node_update)
                self.blackws_nodes.remove(node)
                self.buffer_nodes.append(node)
    
    def movement_options(self, ev = None):
        if ev == None: 
            ev = self.EV_locations[0]
        routes = self.graph.edges(ev)
        return routes

    def update_ev_location(self, ev_loc=None,ev_update = None):
        "ev_update (move up) - edge: (s,t), ev - node: s"
        if ev_update in ["nothing","chargeup","unload"]:
            pass 
        else:
            #if None do for demo
            if ev_loc == None and ev_update == None:
                if ev_loc == None: 
                    ev_loc = self.EV_locations[0]
                ev_index = self.EV_locations.index(ev_loc)
                if ev_update == None:
                    routes = self.graph.edges(ev_loc)
                    ev_update = random.sample(list(routes), 1)[0]
                
                # print(ev)
                # print(f'new location: {ev_update}')
                # print(f'EV_index: {ev_index}')
                if ev_loc == ev_update[0]:
                    new_ev_loc = ev_update[1]
                else: 
                    new_ev_loc = ev_update[0]
                # print(f'new location: {new_ev_loc}')
                self.EV_locations[ev_index] = new_ev_loc
            else:
                # print(type(ev))
                ev_index = self.EV_locations.index(ev_loc)
                if ev_loc == ev_update[0][0]:
                    new_ev_loc = ev_update[0][1]
                else: 
                    new_ev_loc = ev_update[0][0]
                # print(f'new location: {new_ev_loc}')
                self.EV_locations[ev_index] = new_ev_loc
    
    def plot_nodes(self, update = True):
        if update == True: 
            self.color_map = []
            self.size_map = []
            self.label_map = {}
            # self.shape_map = []
            # print(f'current locations: {self.EV_locations}')
            for key, val in self.node_status.items():
                if val == 1:
                    self.color_map.append('darkgrey')
                    # self.shape_map.append(300)
                elif val == 2:
                    self.color_map.append('lightgrey')
                    # self.shape_map.append(300)
                elif val == 4:
                    self.color_map.append('yellow')
                    # self.shape_map.append(300)
                elif val == 5:
                    self.color_map.append('green')
                else:
                    self.color_map.append('blue')

                if key in (self.EV_locations):
                    # print(f'current location: {key}')
                    self.size_map.append(1000)
                    idx = self.EV_locations.index(key)
                    # self.label_map.append(key)
                    # self.label_map.append(self.agents[idx].current_battery)
                    self.label_map[key] = f'Current Charge {(round(self.agents[idx].current_battery,2))}/{(self.agents[idx].MAX_BATTERY)}' 
                else:
                    self.size_map.append(300)
                    # self.label_map.append(key)
                    # self.label_map.append(" ")
                    self.label_map[key] = " "

        else:       
            pass

        label_map = dict(self.label_map)
        edge_labels = nx.get_edge_attributes(self.graph,'cost')
        #set postions of graph for consistent ploting
        # pos=nx.spring_layout(self.graph)
        # pos = nx.spectral_layout(self.graph, weight="cost")
        pos =  nx.circular_layout(self.graph)
        nx.draw_networkx_edge_labels(self.graph,pos = pos, edge_labels= edge_labels )
        nx.draw(self.graph,pos = pos, node_color=self.color_map, node_size = self.size_map, with_labels=True )
        for l in pos:  # raise text positions
            pos[l][1] += 0.25
        nx.draw_networkx_labels(self.graph, pos=pos,labels = label_map, verticalalignment="top")
        
    def _plot_nodes_c(self, update = True):
        if update == True: 
            self.color_map = []
            for key, val in self.node_status.items():
                self.color_map.append(f'C{val}')
                if key in self.EV_locations:
                    # print(key)
                    self.size_map.append(1000)
                else:
                    self.size_map.append(300)
        else:       
            pass
        nx.draw(self.graph, node_color=self.color_map, node_size = self.size_map, with_labels=True)
    
    def gnp_random_connected_graph(self, n, p = .5):
        """ 
        Generates a random undirected graph, similarly to an Erdős-Rényi 
        graph, but enforcing that the resulting graph is conneted 
        """
        edges = combinations(range(n), 2)
        G = nx.Graph()
        G.add_nodes_from(range(n))
        if p <= 0:
            return G
        if p >= 1:
            return nx.complete_graph(n, create_using=G)
        for _, node_edges in groupby(edges, key=lambda x: x[0]):
            node_edges = list(node_edges)
            random_edge = random.choice(node_edges)
            G.add_edge(*random_edge)
            for e in node_edges:
                if random.random() < p:
                    G.add_edge(*e)
        return G


if __name__ == "__main__":
    n = 5 
    env = graph_env(n)
    # env.get_available_action()
    env.step()
    # print(env.actions)
    # print(env.node_status)
    # for i in range(5):
    #     env.plot_nodes()
    #     plt.pause(5)
    #     plt.close()
    #     env.update_ev_location()
# main()


