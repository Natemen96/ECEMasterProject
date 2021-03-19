import json
import os 

print()
print(os.getcwd())

with open('./RL/agent/nissan_leaf.json') as f:
  nissan_leaf = json.load(f)
