import numpy as np
import pandas as pd

class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_min = .95):
        self.actions = actions
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.e_min = e_min #95 % chance of not being random, 05% chance of being random 

    def choose_action(self, observation, ep):
        self.check_state_exist(observation)
        self.update_e_greedy(ep) #sets self.e_greedy
        #greater than epsilon, look at qtable other random 
        if np.random.uniform() > self.e_greedy:
            state_action = self.q_table.loc[observation, :]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'last':
            q_target = r + self.reward_decay * self.q_table.loc[s_, :].max()
        else:
            q_target = r
        self.q_table.loc[s, a] += self.learning_rate * (q_target - q_predict)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(pd.Series([0] * len(self.actions), 
                                                        index=self.q_table.columns, 
                                                        name=state))
    def update_e_greedy(self, ep):
        #linear decay, least reandom after 200 eps
        self.e_greedy = 1 -  min(self.e_min, np.log10((ep + 50)/25))
    
    def save_qtable(self,ep,folder = '../../models/Qtables/'):
        self.q_table.to_hdf(folder+f'qtable_ep_{int(ep)}.pickle.h5', key='s')

    def load_qtable(self,qtable_file):
        self.q_table = pd.read_hdf(qtable_file, key='s')

