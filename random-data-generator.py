import csv
import pandas as pd
from datetime import datetime
from pydantic import BaseModel
from enum import Enum, auto
from typing import List
import random
import names


def generate_random_data_for_division(teams: int, players_per_team: int, division: str):

    for x in range(teams * players_per_team):
        number = random.randint(1000,1000+(teams * players_per_team))
        division = division
        score = random.randint(9,45) / 100
        yield  (number,division,score )



players = [x for x in generate_random_data_for_division(8,7, "DIV1") ]

# print(players)
df = (pd.DataFrame(data=players, columns=["player_number", "player_division", "player_score"])
        .sort_values(by=["player_division", "player_number"], axis=0, ascending=False, ignore_index=True, key=None)
        )


df.to_excel("data.xlsx", index=False)
