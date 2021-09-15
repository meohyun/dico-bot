import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!',help_command=None)
token = ('ODg3NTc3MTQ3OTQwNzAwMjEw.YUGKog.rqmwApEu5jKxE-kTktjY7mDZmTs')

async def on_ready():
    print(f'부팅 성공: {bot.user.name}!')
    game = discord.Game("Beta Ver")
    await bot.change.presence(status = discord.Status.online,activity = game)

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕하세요")

@bot.command()
async def 봇(ctx):
    msg = ctx.message.content[3:]
    await ctx.send(msg)

@bot.command()
async def 종료(ctx):
    await ctx.quit()

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("정확한 명령어를 입력해주세요.")

bot.run(token)