import requests
import json
import pandas as pd

api_key =  'api'

username = input("")
player_num = []
gameId_data = []
champion_id = []
name = []
player_name = []
blue_player_name=[]
red_player_name = []

################################################################################################
# URL,req,req_json

user_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + username

req = requests.get(user_url,headers={"X-Riot-Token":api_key})
req_json = json.loads(req.text)

account_id = req_json['accountId']

match_url = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account_id

req_2 = requests.get(match_url,headers={"X-Riot-Token":api_key})
req_2_json = json.loads(req_2.text)


# 매치 데이터를 pandas 프레임으로 변환
match_df = pd.DataFrame(req_2_json)

# 매치 id를 넣는다.
for i in range(len(match_df)):
    gameId_data.append(match_df['matches'][i]['gameId'])

# 최근 전적 중 어느 전적을 가져올지 정함
match_url2 = "https://kr.api.riotgames.com/lol/match/v4/matches/" + str(gameId_data[0])

req_3 = requests.get(match_url2,headers={"X-Riot-Token":api_key})
req_3_json = json.loads(req_3.text)

champion_url = "https://ddragon.leagueoflegends.com/cdn/11.18.1/data/ko_KR/champion.json"

req_4 = requests.get(champion_url,headers={"X-Riot-Token":api_key})
req_4_json = json.loads(req_4.text)

champion_df = pd.DataFrame(req_4_json)


########################################################################################################



# 검색한 플레이어는 몇번째 플레이어 인가?
for i in range(10):
    if req_3_json['participantIdentities'][i]['player']['summonerName'] == username:
        player_num.append(req_3_json['participantIdentities'][i]['participantId'])

# 검색한 플레이어는 해당 게임을 이겼는가?
for i in range(10):
    if req_3_json['participants'][i]['participantId'] == player_num[0]:
        win_or_lose = req_3_json['participants'][i]['stats']['win']

        if win_or_lose == True:
            print("승리")
        else:
            print("패배")
        


# 게임 플레이어 이름
for i in range(10):
    player_name.append(req_3_json['participantIdentities'][i]['player']['summonerName'])
    # if req_3_json['participants'][i]['teamId'] == 100:
    #     blue_player_name.append(req_3_json['participantIdentities'][i]['player']['summonerName'])
    # else:
    #     red_player_name.append(req_3_json['participantIdentities'][i]['player']['summonerName'])


# 챔피언 정보
for i in range(10):
    champion_id.append(req_3_json['participants'][i]['championId'])



# 챔피언 고유번호 -> 챔피언 이름
for i in range(len(champion_df)):
    # 챔피언 이름과 고유번호를 하나의 리스트에 넣음
    name.append([champion_df['data'][i]['name'],champion_df['data'][i]['key']])

for i in range(len(name)):
    for j in range(len(champion_id)):
        # 리스트 안에서 챔피언 고유번호로 챔피언 이름을 찾고, 매치에서 해당 챔피언을 사용한 유저의 닉네임을 출력
        if name[i][1] == str(champion_id[j]):
            print(name[i][0],player_name[j])
         