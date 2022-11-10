import csv
import pandas as pd
from datetime import datetime
from pydantic import BaseModel
from enum import Enum, auto
from typing import List
import random
import names

class Division(Enum):
    U05B = auto()
    U06B = auto()
    U08B = auto()
    U10B = auto()
    U12B = auto()
    U14B = auto()
    U16B = auto()
    U19B = auto()
    U05G = auto()
    U06G = auto()
    U08G = auto()
    U10G = auto()
    U12G = auto()
    U14G = auto()
    U16G = auto()

class DivisionConfig(BaseModel):
    division: Division
    teams: int
    players_per_team: int
    
class Score(BaseModel):
    player_number: int
    player_name: str
    player_team: str
    player_division: Division
    player_score: int


def load_data_from_file() -> List[Score]:
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        scores = List[Score]
        for each_row in reader:
           scores.append(Score(*each_row) )

def generate_random_data_for_division(config: DivisionConfig):

    for x in range(config.teams * config.players_per_team):
        number = random.randint(1,20)
        name = names.get_full_name()
        team = f"Team { random.randint(1,config.teams)}"
        division = config.division.name
        score = random.randint(20,100)
        yield  (number,name,team,division,score )

if __name__ == "__main__":
    
    config = [
        DivisionConfig(Division.U05B, teams=8, players_per_team=5),
        DivisionConfig(Division.U05G, teams=4, players_per_team=5),
        DivisionConfig(Division.U06B, teams=8, players_per_team=5),
        DivisionConfig(Division.U06G, teams=4, players_per_team=5),
        DivisionConfig(Division.U08B, teams=20, players_per_team=5),
        DivisionConfig(Division.U08G, teams=16, players_per_team=5),
        DivisionConfig(Division.U10B, teams=12, players_per_team=5),
        DivisionConfig(Division.U10G, teams=10, players_per_team=5),
        DivisionConfig(Division.U12B, teams=8, players_per_team=5),
        DivisionConfig(Division.U12G, teams=8, players_per_team=5),
        DivisionConfig(Division.U14B, teams=22, players_per_team=5),
        DivisionConfig(Division.U14G, teams=18, players_per_team=5),
        DivisionConfig(Division.U16B, teams=0, players_per_team=0),
        DivisionConfig(Division.U16G, teams=18, players_per_team=5),
        DivisionConfig(Division.U19B, teams=0, players_per_team=0),

    ]
    
    for d in config:
        players = [x for x in generate_random_data_for_division(d) ]
    
    
    # print(players)
    df = (pd.DataFrame(data=players, columns=["player_number", "player_name", "player_team", "player_division", "player_score"])
         .sort_values(by=["player_division", "player_team", "player_team", "player_number"], axis=0, ascending=False, ignore_index=True, key=None)
         )
    print(df)

# external_data = {
#     'id': '123',
#     'signup_ts': '2019-06-01 12:22',
#     'friends': [1, 2, '3'],
# }
# user = User(**external_data)
# print(user.id)
# #> 123
# print(repr(user.signup_ts))
# #> datetime.datetime(2019, 6, 1, 12, 22)
# print(user.friends)
# #> [1, 2, 3]
# print(user.dict())
# """
# {
#     'id': 123,
#     'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
#     'friends': [1, 2, 3],
#     'name': 'John Doe',
# }
# """