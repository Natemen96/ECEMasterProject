# ECEMasterProject
<!-- ## RL Scenario -->

![Visual of a Node Network, 3 nodes, 3 layers connected in pairs](visuals/demogif.gif)

## Purpose

In situations of natural disasters/phenomenons, blackouts can occur. To combat this, EV (electric vehicles) drivers can use their vehicles as batteries for customers/ clients. To simulate the difficulty of this challenge of getting to as much customers as possible until the blackout period is over, a RL environment was created. This environment features random scenarios based on node network size, amount of the houses (can't be larger than node size), blackout data, and housing models to try simulate in a high level matter.

## Task for Agent

Start at "Home" (a node) travel to each location in exchange for energy (main resource for EV),
unload energy in exchange for energy, travel back to home in exchange for energy. The agent can restore energy at "Home".
Once power is restored in at a node with a power charging station, the agent can restore energy there as well. Some nodes will be empty debating on parameters.

## Environment Overview
 <!-- #TODO -->
## Agent Overview 
 <!-- #TODO -->

## Reward

Reward given for unloading, recharging.
Diversity of power restoration will result in more reward.
Reward lost for running out of energy.
Episode is over when EV is out of energy or network is completely powered.

## Action & State Space

    Each Agent will have 24 actions per ep by default.

    e+2 Actions:
        e - Move (at Cost) to Node if possible
        1 - Unload (at cost)
        1 - Recharge (no cost, expect an action)

    2n+c States:
        n - Statuses of Each Node
            Key - Assignment
            0 - Buffer
            1 - Blackout
            2 - Blackout with Solar
            3 - Powered
            4 - Charging Station
            5 - Home

        n - Cost of each edge
        
        c - Charge State 
        
    where n is the number of nodes, e is the number of edges
    <!-- , and i is the cost.  -->

## Logic

Each nodes was designed to be based on a house dataset. Some houses that are solar powered will need less power from EVs compared to non-solar powered homes. The cost will be derive from the housing model.

<!-- This can be modified by passing in a .npy file to the enviroments `nonsolarhouse_data_paths = [path_to_data]` -->

Percentage of blackout based on texas blackout data, as well as change per day.

At a minimum a **Q-Learning** was used to find the best solutions.

## Scalability

Can be scaled to multiple EV (MARL would be needed), & a larger network. This feature has not been fully tested and is likely very buggy.

## Extras Ideas

Some edges can be blocked off and restored later as days pass (simulate for natural disasters)

DRL and Classic Optimization techniques

Debug for MARL

Convert to OpenAI environment

## Acknowledgements

Thank you to [Professor Qin](https://engineering.purdue.edu/ECE/People/ptPeopleListing?group_id=2571&resource_id=246563) of my alma mater, Purdue University for his amazing support and sharing his expertise for this project.

## Authors

- [@Natemen96](https://www.github.com/Natemen96)

## Demo

Insert gif or link to demo


<!-- ## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0) -->
  