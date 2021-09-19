import requests
import json
import pandas as pd
from datetime import datetime

api_key = 'api'

username = input("")
user_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + username

req = requests.get(user_url,headers={"X-Riot-Token":api_key})
req_json = json.loads(req.text)

account_id = req_json['accountId']

match_url = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account_id

req_2 = requests.get(match_url,headers={"X-Riot-Token":api_key})
req_2_json = json.loads(req_2.text)


my_matches = req_2_json['matches'][0]['timestamp']
game_time = datetime.fromtimestamp(my_matches)
print(game_time)

