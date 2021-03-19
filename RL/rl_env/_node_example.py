# https://plotly.com/python/network-graphs/
# https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python

# import plotly.graph_objects as go

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
n = 10
theta = .5
G = nx.random_geometric_graph(n, theta)
# G = nx.geographical_threshold_graph(n, theta)


# nx.draw_spring(G)
# plt.show()
# plt.hist([v for k,v in nx.degree(G)])
# plt.show()
# plt.hist(nx.centrality.closeness_centrality(G).values())
# plt.show()
nx.diameter(G)
print("Hello World")
