import discord
import datetime as dt

client = discord.Client()

token = 'input your token'

# 봇 로그인
@client.event
async def on_ready():
    print('다음으로 로그인합니다.')
    print(client.user.name)
    print(client.user.id)
    print('=======================')

current_time = dt.datetime.now()

@client.event
async def on_message(message):
    if message.content == "!시간":
        await message.channel.send(current_time)

client.run(token)