# ECEMasterProject

- [ECEMasterProject](#ecemasterproject)
  - [Run Locally](#run-locally)
  - [Installation](#installation)
  - [Purpose](#purpose)
  - [Demo](#demo)
  - [Task for Agent](#task-for-agent)
  - [Environment Overview](#environment-overview)
  - [Agent Overview](#agent-overview)
  - [Reward](#reward)
  - [Action & State Space](#action--state-space)
  - [Logic](#logic)
  - [Scalability](#scalability)
  - [Optimizations](#optimizations)
  - [Extras Ideas](#extras-ideas)
  - [Lessons Learned](#lessons-learned)
  - [Acknowledgements](#acknowledgements)
  - [Authors](#authors)

## Run Locally

Clone the project

```bash
  git clone https://github.com/Natemen96/ECEMasterProject.git
```

Go to the project directory

```bash
  cd ECEMasterProject
```

```bash
  python RL/main.py
```

## Installation

WARNING: This is a large install (~2GB). Depending on your set up, you may find it easier to install the package yourself. The list can be found in the `conda_env` folder. See 'conda_env/rl_window.yml' for the most up to date package list.

The conda environment follow this installation please 1st download [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

After conda is install do the following to set up the environment

```bash
  conda env create -f conda_env/rl_windows.yml #
  mv rl_windows rl_env #or any name you prefer
  conda activate rl_env #verify it work 
```

make sure to run the program within the conda env.

## Purpose

In situations of natural disasters/phenomenons, blackouts can occur. To combat this, EV (electric vehicles) drivers can use their vehicles as batteries for customers/ clients. To simulate the difficulty of this challenge of getting to as much customers as possible until the blackout period is over, a RL environment was created. This environment features random scenarios based on node network size, amount of the houses (can't be larger than node size), blackout data, and housing models to try simulate in a high level matter.

## Demo

![Demo of RL environment + random agent in action](visuals/demogif.gif)
Example of an random agent in action.

Load represents the power needed at the moment from the node.

Current Charge represents the power the agent (or car) has.

Values on edges represents the miles of the edge cost to go through.

Blue node represents buffers. Green node represents homes. Grey node represent blackout out node.

More details can be found in [Action & State Space](#action--state-space) section.

## Task for Agent

Start at "Home" (a node) travel to each location in exchange for power (main resource for EV),
unload power in exchange for reward, travel back to home in exchange for power. The agent can restore power at "Home" and earn more reward depending on how much power it got back. The more power it restore the most it's rewarded.

Once power is restored in at a node with a power charging station, the agent can restore energy there as well. Some nodes will be empty depending on parameters.

## Environment Overview

```txt
graph_env: Randomly generated a fully connected graph n nodes

Args:
    n (int, optional): [number of nodes]. Defaults to 5.
    numofhome (int, optional): [number of homes for agent starting 
    point]. Defaults to 1.
    numofblackout (int, optional): [number of houses with blackout]. 
    Defaults to 1.
    numofblackoutws (int, optional): [number of blackout houses with 
    solarpower]. Defaults to 0.
    numofchargingstation (int, optional): [number of charging 
    station]. Defaults to 0.
    max_actions (int, optional): [max number of action can be done 
    times 7.  By default 3 (7) = 21]. Defaults to 3.
    blackout_str (str, optional): [Reads Blackout data from npy file]
    . Defaults to 'Brazoria'.
    agents (list, optional): [Agent objects]. Defaults to [None].
    nonsolarhouse_data_paths (list, optional): [Path for npy file 
    with nonsolar data info. Added to a node per path.]. Defaults to 
    [None].
    solarhouse_data_paths (list, optional): [Path for npy file with 
    solarhouse data info. Added to a node per path.]. Defaults to 
    [None].
    data_sample (int, optional): [how many data sample it take from 
    data in paths, samples taken evenly throughout data. By default 
    (0/6. 1/6 ... 6/6 0/6 ...) sample]. Defaults to 6.
```

## Agent Overview

```txt
BasicAgent: Basic Agent that act as skeleton for other agent. Won't work by it's self.

Args:
    car ([dict]): [car information in the form of a python dictionary]
```

```txt
SmartQLAgent: Smart Agent that uses Qtable to make decisions

Args:
    car ([dict]): [car information in the form of a python dictionary]
    sample_rate (int, optional): [decides how often a sample of the
    qtable is taken. If left to default it's every 1/100 of total ep]
    . Defaults to 100.
    qtabletraining (bool, optional): [Flag for turning qtable 
    training on]. Defaults to True.
    quiet (bool, optional): [Flag for turning data collection on]. 
    Defaults to True.
```

```txt
RandomDataAgent: Used for data collection of random agent. Doesn't 
use Observation.

Args:
    car ([dict]): [car information in the form of a python 
    dictionary]
```

## Reward

Reward given for unloading, recharging.
Diversity of power restoration will result in more reward.
Reward lost for running out of energy.
Episode is over when EV is out of energy or network is completely powered.

## Action & State Space

    Each Agent will have 24 actions per ep by default.

    e+2 Actions:
        e - Move (at cost) to Node if possible
        1 - Unload (at cost)
        1 - Recharge (no cost, expect an action)

    2*n + 6*n + 300*n + 400*c States:
        n - Statuses of Each Node
            Key - Assignment
            0 - Buffer (Blue)
            1 - Blackout (Darkgrey)
            2 - Blackout with Solar (Lightgrey)
            3 - Powered (Blue)
            4 - Charging Station (Yellow)
            5 - Home (Green)

        n - Cost of each edge

        n - Is the path reachable or not? 
            0 - No 
            1 - Yes
        
        c - Charge State 
        
    where n is the number of nodes states, e is the number of edges, and c number of is Charge states 

## Logic

Each nodes was designed to be based on a house dataset. Some houses that are solar powered will need less power from EVs compared to non-solar powered homes. The cost of house node can be derive from the housing data.

Percentage of blackout based on texas blackout data, as well as change per day.

At a minimum a **Q-Learning** was used to find the best solutions.

## Scalability

Can be scaled to multiple EV (MARL would be needed), & a larger network. MARL has not been fully tested and is likely very buggy.


## Optimizations

During a test run of 50k Eps the smart agent that was support with Qtables had 263.13% improvement compared to a random agent (that does random actions).

## Extras Ideas

Some edges can be blocked off and restored later as days pass (simulate for natural disasters)

Add testing

DRL and Classic Optimization techniques

Debug for MARL

Convert to OpenAI environment


## Lessons Learned

Learned more about making DL/ML models.

Learned more about data analysis from exploring data and results from DL/ML training.

Learned about networkx and it's capabilities for graph theory related for project.

Learned more about making reinforcement learning environment and agents.

Learned a bit more about data scraping as I need to scrap blackout data during the [Texas Blackout](https://en.wikipedia.org/wiki/2021_Texas_power_crisis)

Learned how to make a gif using images in python.

## Acknowledgements

Thank you to [Professor Qin](https://engineering.purdue.edu/ECE/People/ptPeopleListing?group_id=2571&resource_id=246563) of my alma mater, Purdue University for his amazing support and sharing his expertise for this project.

Thank you to [DataPort](https://pecanstreet.org/dataport) and [Pecan Street](https://github.com/Pecan-Street) for providing housing data to build models with.

Thank you to [Matt Leacock](https://en.wikipedia.org/wiki/Matt_Leacock) the creator of the board game, [Pandemic](https://en.wikipedia.org/wiki/Pandemic_(board_game)) for inspiring this Reinforcement Learning Environment.

## Authors

- [@Natemen96](https://www.github.com/Natemen96)

<!-- ## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0) -->
  