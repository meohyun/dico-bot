import discord
from discord.ext import commands
import random 
import time
import requests
import json
from foods_choice import foods 

client = discord.Client()
bot = commands.Bot(command_prefix='!',help_command=None)
token = ('')
lol_api_key = ''

async def on_ready():
    print(f'부팅 성공: {bot.user.name}!')
    game = discord.Game("Beta Ver")
    await bot.change.presence(status = discord.Status.online,activity = game)


@client.event
async def on_message(message):
     if message.content.startswith("/검색 "):
        UserName = message.content.replace("/검색 ", "")
        UserInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + UserName
        res = requests.get(UserInfoUrl, headers={"X-Riot-Token":lol_api_key})

        resjs = json.loads(res.text)

        if res.status_code == 200:
            UserIconUrl = "http://ddragon.leagueoflegends.com/cdn/11.3.1/img/profileicon/{}.png"
            embed = discord.Embed(title=f"{resjs['name']} 님의 플레이어 정보", description=f"**{resjs['summonerLevel']} LEVEL**", color=0xFF9900)

            UserInfoUrl_2 = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + resjs["id"]
            res_2 = requests.get(UserInfoUrl_2, headers={"X-Riot-Token":lol_api_key})
            res_2js = json.loads(res_2.text)
        

            if res_2js == []: # 언랭크일때
                embed.add_field(name=f"{resjs['name']} 님은 언랭크입니다.", value="**언랭크 유저의 정보는 출력하지 않습니다.**", inline=False)

            else: # 언랭크가 아닐때
                for rank in res_2js:
                    if rank["queueType"] == "RANKED_SOLO_5x5":
                        embed.add_field(name="솔로랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                           f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)

                    else:
                        embed.add_field(name="자유랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                            f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)

            embed.set_author(name=resjs['name'], url=f"http://fow.kr/find/{UserName.replace(' ', '')}", icon_url=UserIconUrl.format(resjs['profileIconId']))
            await message.channel.send(embed=embed)

        else: # 존재하지 않는 소환사일때
            error = discord.Embed(title="존재하지 않는 소환사명입니다.\n다시 한번 확인해주세요.", color=0xFF9900)
            await message.channel.send(embed=error)

client.run(token)

@bot.command()
async def 로또(ctx):
    await ctx.send("행운의 번호를 추첨중입니다...")
    time.sleep(3)
    num=[]
    for i in range(1,46):
        num.append(i)
    lotto_num = random.sample(num,7)
    lotto_nums = map(str,lotto_num)
    await ctx.send('행운의 번호: '+'  '.join(lotto_nums))

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕하세요")


@bot.command()
async def 숫자야구(ctx):
    global three_numbers
    three_numbers = random.sample(range(1,10),3)
    await ctx.send("숫자야구 게임을 시작합니다!")

@bot.command()
async def 답(ctx,*args):

    s = 0
    b = 0
    quoto_1 = int(args[0]) 
    quoto_2 = int(args[1])
    quoto_3 = int(args[2])
   
   # 입력한 수 중 1개가 숫자와 위치가같다면 - 1strike
    if quoto_1== three_numbers[0]:
        s = 1
        # 입력한 수 중 2개가 숫자와 위치가 같다면 - 2strike
        if quoto_2 == three_numbers[1]:
            s = 2
            # 입력한 수 중 3개가 숫자와 위치가 같다면 - success
            if quoto_3 == three_numbers[2]: 
                s = 3
                await ctx.send("정답입니다!")
                
        elif quoto_3 == three_numbers[2]:
            s = 2
    elif quoto_2==three_numbers[1]:
        s = 1
        if quoto_3 == three_numbers[2]:
            s = 2
    elif quoto_3 == three_numbers[2]:
        s = 1
    
    # 입력한 수가 위치는 다르지만 숫자가 같다면 - 1BALL
    if not quoto_1 == three_numbers[0] and quoto_1 in three_numbers :
        b = 1
        if not quoto_2 == three_numbers[1] and quoto_2 in three_numbers :
            b= 2
            if not quoto_3 == three_numbers[2] and quoto_3 in three_numbers :
                b= 3
        elif not quoto_3 == three_numbers[2] and quoto_3 in three_numbers :
            b= 2
    elif not quoto_2 == three_numbers[1] and quoto_2 in three_numbers :
        b = 1
        if not quoto_3 == three_numbers[2] and quoto_3 in three_numbers :
            b= 2
    elif not quoto_3 == three_numbers[2] and quoto_3 in three_numbers :
        b = 1
    
    await ctx.send("{} 스트라이크 {}볼".format(s,b))

@bot.command()
@commands.is_owner()
async def 종료(ctx):
    exit()

@bot.command()
async def 메뉴(ctx):
    menu = random.sample(foods,1)
    await ctx.send("오늘의 추천메뉴는 {} 입니다".format(''.join(menu)))

@bot.command()
async def 봇(ctx):
    msg = ctx.message.content[3:]
    await ctx.send(msg)

@bot.command()
async def 더하기(ctx ,*args):
    plus = int(args[0]) + int(args[1])
    await ctx.send(plus)

@bot.command()
async def 곱하기(ctx,*args):
    multiply = int(args[0])*int(args[1])
    await ctx.send(multiply)
    
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("정확한 명령어를 입력해주세요.")

bot.run(token)
