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
        channel = message.channel

        smu_id = message.content[5:14]
        smu_pw = message.content[15:]

        login_url = 'https://ecampus.smu.ac.kr/login/index.php'  #로그인 창 주소
        class2021_url = 'https://ecampus.smu.ac.kr/local/ubion/user/?year=2021&semester=20'  #강의 인덱스 가져오기 위한 주소
        url_lst = []
        url_lst_assign = []
        url_lec_lst = []

        user_info = {}

        user_info['username'] = smu_id
        user_info['password'] = smu_pw

        with requests.Session() as s:
            #필요한 주소들 & selecter들 미리 설정
            request = s.post(login_url, data = user_info)
            request3 = s.post(class2021_url, data = user_info)
            source = request3.text
            soup = BeautifulSoup(source,'html.parser')
            items = soup.find_all("a", {"class", "coursefullname"})

            #강의 제목 끌어오기
            class_name_lst = []
            for name in items:
                arrange = name.get_text()
                class_name_lst.append(arrange)     

            #url에 있는 강의가 갖고 있는 id코드 크롤링하기
            if (request.status_code == 200):
                bs = BeautifulSoup(request3.text, 'html.parser')

                lectures = bs.select('#region-main > div > div > div.course_lists > div > table > tbody > tr > td > div > a')

                class_list = []
                for lecture in lectures:
                    class_list.append(str(lecture))
                lst = []
                for i in class_list:
                    index = i.find('id')
                    lst.append(int(i[index+3:index+8]))
                count = len(lst)
                for i in range(count):
                    url_lst_assign.append('https://ecampus.smu.ac.kr/mod/assign/index.php?id='+str(lst[i]))
                    url_lst.append('https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id='+str(lst[i]))
                    url_lec_lst.append('https://ecampus.smu.ac.kr/course/view.php?id='+str(lst[i]))

            if (request.status_code == 200):
                for i in range(count):
                    request4 = s.post(url_lec_lst[i])
                    bs = BeautifulSoup(request4.text, 'html.parser')
                    deadlines = bs.find_all('span', {'class', 'text-ubstrap'})

            deadline_lst = []
            for deadline in deadlines:
                deadline_lst.append(deadline.text)

            for i in deadline_lst:
                index = i.find('~')
                i = i[index+2:]

            #강의진도현황크롤링하기
            if (request3.status_code == 200):
                value_lst = []
                for i in range(count):
                    request3 = s.post(url_lst[i])
                    name_lst = []
                    rate_list = []
                    a_li = [] # 진도율
        
                    bs  = BeautifulSoup(request3.text, 'html.parser')
                    lecture_name = bs.find_all("td", {"class", "text-left"})
                    rates = bs.find_all("td", {"class", "text-center"})
                    
                    for name in lecture_name:
                        name_lst.append(name.text.strip())
                    name_lst = name_lst[3:]

                    for rate in rates:
                        rate_list.append(str(rate.text))

                    for word in rate_list:
                        if '%' in word:         # 진도율만 뽑아내기 위해서 %가 포함된 부분만 검색
                            a_li.append(word)
                        elif word == '-':
                            a_li.append(word)
                    
                    size = len(a_li)

                    i += 1
                    absent_lst = []
                    value = ''
                    for i in range(0, size):
                        if float(a_li[i][:-1]) < 100:
                            string = name_lst[i] + ' / 진도율: ' + a_li[i] + ' / 마감일: ' + deadline_lst[i]
                            absent_lst.append(string)
                                
                    if len(absent_lst) == 0:
                        value_lst.append("모든 강의를 100% 출석하였습니다. 아주 훌륭해요!!")
                    else:
                        for i in absent_lst:
                            value += (i + '\n')
                        value_lst.append(value)
                                
            embed = discord.Embed(title = "진도율 100% 미만 강의 목록", description = "(2021학년도 1학기)", color = 0xB2EBF4)
            for i in range(count):
                embed.add_field(name = class_name_lst[i], value = value_lst[i], inline = False)
            await message.channel.send(embed = embed)


client.run(token)
