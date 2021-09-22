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
lol_api_key = ('')


async def on_ready():
    print(f'부팅 성공: {bot.user.name}!')
    game = discord.Game("Beta Ver")
    await bot.change.presence(status = discord.Status.online,activity = game)

@bot.command()
async def 로또(message):
    await  message.send("행운의 번호를 추첨중입니다...")
    time.sleep(3)
    num=[]
    for i in range(1,46):
        num.append(i)
    lotto_num = random.sample(num,7)
    lotto_nums = map(str,lotto_num)

    if message.content == "!로또":
        channel = message.channel
        
        embed = discord.Embed(title='로또',description= '행운의 번호 입니다.', color= 0x00ff00)
        embed.add_field(name="행운의번호",value= lotto_nums,inline=True)
    
        await channel.send(embed=embed)

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