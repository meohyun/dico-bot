import discord
from discord.ext import commands
import random 
import time
from foods_choice import foods 

bot = commands.Bot(command_prefix='!',help_command=None)
token = ('토큰')
    

async def on_ready():
    print(f'부팅 성공: {bot.user.name}!')
    game = discord.Game("Beta Ver")
    await bot.change.presence(status = discord.Status.online,activity = game)

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