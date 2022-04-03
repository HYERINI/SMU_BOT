import asyncio
import discord
import requests
from bs4 import BeautifulSoup

client = discord.Client()

token = 'input your token'

# 봇 로그인
@client.event
async def on_ready():
    print('다음으로 로그인합니다.')
    print(client.user.name)
    print(client.user.id)
    print('=======================')

@client.event
async def on_message(message):
    if message.author.bot:
        return None
    if message.content == '!안녕':
        channel = message.channel
        await channel.send('안녕하세요!')
    if message.content == '!설명':
        if message.author.dm_channel:
            await message.author.dm_channel.send('DM 채널이 있어서 보내봤어요')
        elif message.author.dm_channel is None:
            channel = await message.author.create_dm()
            await channel.send('DM 채널이 없어서 만들고 보냈어요')
    if message.content.startswith('!로그인'):
        smu_id = message.content[5:14]
        smu_pw = message.content[15:]

        login_url = 'https://ecampus.smu.ac.kr/login/index.php'
        class2021_url = 'https://ecampus.smu.ac.kr/local/ubion/user/?year=2021&semester=10'
        class1_url = 'https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id=60021'

        user_info = {}

        user_info['username'] = smu_id
        user_info['password'] = smu_pw

        with requests.Session() as s:
            request = s.post(login_url, data = user_info)
            request2 = s.post(class1_url, data = user_info)
            if (request.status_code == 200):
                bs = BeautifulSoup(request2.text, 'html.parser')

        lecture_name = bs.find_all("td", {"class", "text-left"})

        name_lst = []
        for name in lecture_name:
            name_lst.append(name.text.strip())
        result = name_lst[3:]

        channel = message.channel
        await channel.send(result)

client.run(token)