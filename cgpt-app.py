import numpy as np
from scipy.optimize import linprog
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import seaborn as sns
import time

def find_teams(scores, n, team_size):
    # Number of players
    m = len(scores)

    # Objective function coefficients (maximize total score)
    c = np.array(scores)

    # Constraint matrix (each player can only be assigned to one team)
    A = np.eye(m)

    # Constraint bounds (each player can only be assigned to one team)
    b = np.ones(m)
    
    # Team constraints (teams must have exactly `team_size` players)
    A_eq = np.zeros((n, m))
    
    for i in range(n):
        A_eq[i, i * team_size : (i + 1) * team_size] = np.ones(team_size)

    # Team constraint bounds (teams must have exactly `team_size` players)
    b_eq = np.ones(n) * team_size

    # Decision variable bounds (0 <= x <= 1)
    bounds = [(0, 1) for _ in range(m)]

    # Solve the linear programming problem
    res = linprog(c, A, b, A_eq, b_eq, bounds=bounds, method="highs")

    # Extract the team assignments
    team_assignments = np.round(res.x).astype(int)

    return team_assignments


data_pd = pd.read_csv("data/Ratings Fall 2022.10UB.csv",index_col=1, dtype={"player_number":np.intp})

data_pd["slot#"] = None

# Example usage
# scores = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
scores = data_pd["player_score"].values
print("scores--->>>>",scores)
n = 11
team_size = len(scores) // n
print(f"team_size: {team_size}")
team_assignments = find_teams(scores, n, team_size)

# Print the team assignments
for i in range(n):
    team = [j for j in range(len(scores)) if team_assignments[j] == i]
    print(f"Team {i}: {[scores[j] for j in team]}")
