#!/usr/bin/env python
# coding: utf-8

# In[24]:


# goals
# variables
# constraints
# algos:
#   - GRG non linear (smooth nonlinear problems)
#   - LP Simplex (linear)
#   - Evolutionary (non-smooth problems)

# objective:
#    - even teams scores

# variables:
#    - Team size
#    - # of players
#    - player score (id, score)

# constraints:
# 1. player can be only on one team
# 2. team can be less but not more than max allowed
# 3. All players have to be used

#https://github.com/nicknochnack/LinearProgrammingBasics/blob/master/LP%20Notebook.ipynb


# In[25]:


import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import seaborn as sns
import time


# In[26]:

file = "Ratings Fall 2022"

data = pd.read_excel(f"{file}.xlsx",  
                     dtype={"player_number":int,  "player_score": int, "player_rating":float, "player_division":str})

print(data)
divisions = data.groupby("player_division")

for key, rows in divisions:
    print(f"Writing {key} ...")
    df = pd.DataFrame(rows, columns=["player_division","player_number","player_score", "player_rating"])
    df.to_csv(f"data/{file}.{key}.csv", index=False)
# %%
