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


data = pd.read_excel("test_data_Division.U05B.xlsx", index_col=0, dtype={"row#":int, "player_number":int, "player_name":str, "player_division":str, "player_score": int})
data_pd = pd.DataFrame(data[["player_number","player_division", "score_reduced"]])

print(len(data_pd))


# In[27]:


import random as rnd
from typing import Union

def top_slice(roster: pd.DataFrame, slices:int, size:int) -> pd.DataFrame:
    roster_mean = roster["score_reduced"].mean()
    
    selection = roster[roster["score_reduced"] > roster_mean].iloc[:slices]
    
    for index, row in selection.iterrows():
        selection.at[index, "slot#"] = index
    
    return selection

def bottom_slice(roster: pd.DataFrame, slices:int, size:int) -> pd.DataFrame:
    roster_mean = roster["score_reduced"].mean()
    
    selection = roster.loc[roster["score_reduced"] <= roster_mean].copy().tail(size)
    selection = selection.reset_index()
    
    for i in range(0, selection.count()[0]):
        selection.at[i, "slot#"] = i
    
    return selection
        
def shuffle(roster: pd.DataFrame, slices:int, size:int) -> pd.DataFrame:
    
    roster["slot#"] = -1
    sorted = roster.sort_values(by=["score_reduced"],axis=0, ascending=False)
    
    top    = top_slice(sorted, slices, size)
    
    bottom = bottom_slice(sorted, slices, size)
        
    selector = pd.concat( [top, bottom] ) 
        
    rest = sorted.iloc[top.count()[0]:bottom.count()[0]].sample(frac=1)
    
    data = pd.concat( [selector, rest] )
    # return selector
    return  data

def slicer(data: pd.DataFrame, slices: int, size: int) -> pd.DataFrame:
    size = size - 1
    for i in range(0, ((slices * size) - size), size):
        slice = pd.DataFrame(data.iloc[i:i+size])
        
        if -1 in slice["slot#"].values:
            slice["slot#"]= int(i/size)
        
        yield slice

def generator(slices: int, size: int) -> List[pd.DataFrame]:
     teams = [i for i in slicer(shuffle(data_pd, slices, size), slices, size)]
     return teams
 
def solver(teams: int, players: int) -> Union[float, pd.DataFrame]:
    teams = generator(teams, players)
    means =[]
    for t in teams:
        t_mean = t["score_reduced"].mean()
        means.append( { "team": t.iloc[0]["slot#"], "mean": t_mean} )

    means_pd = pd.DataFrame(means)
    stdev = means_pd["mean"].std() # <-- minimize this
    return (stdev, teams)


# In[28]:


def main():
    league_teams = 8
    players_per_team = 7
    roster_mean = data_pd["score_reduced"].mean()

    min_min = 100000
    
    selection: List[pd.DataFrame] = None

    for i in range(0, min_min):
        std, teams = solver(league_teams, players_per_team)
        selection = teams
        if std < min_min:
            min_min = std
            pd.concat(teams).to_csv("./solution.csv")
            slots = pd.concat(teams)[["slot#", "score_reduced"]].groupby(["slot#"]).mean(["score_reduced"])
            slots.plot.bar(rot=0)
            plt.show()
            print(f"Itteration: {i} min: {min_min}")
        
        
    print("roster_mean", roster_mean)
    print("min_min", min_min)

    solution = pd.concat(selection)
    solution.to_csv("./solution.csv")

    slots = solution[["slot#", "score_reduced"]].groupby(["slot#"]).mean(["score_reduced"])
    
    ax = slots.plot(kind="bar",  rot=0, animated=True,fill=False)
    ax.set_title("Distribution")
    plt.show()
    
    


# In[29]:


# if __name__ == "__main__":
main()


