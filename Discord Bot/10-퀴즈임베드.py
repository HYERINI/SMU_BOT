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
        lst2 = []

        user_info = {}

        user_info['username'] = smu_id
        user_info['password'] = smu_pw

        with requests.Session() as s:
            request = s.post(login_url, data=user_info)
            request3 = s.post(class2021_url, data=user_info)
            source = request3.text
            soup = BeautifulSoup(source, 'html.parser')
            items = soup.find_all("a", {"class", "coursefullname"})

            # 강의 제목 끌어오기
            class_name_lst = []
            for name in items:
                arrange = name.get_text()
                class_name_lst.append(arrange)

            # 강의별 퀴즈 url id 추출
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
                    lst2.append('https://ecampus.smu.ac.kr/mod/quiz/index.php?id='+str(lst[i]))

            if (request.status_code == 200):
                value3_lst = []
                for i in range(count):
                    request5 = s.post(lst2[i])

                    bs = BeautifulSoup(request5.text, 'html.parser')

                    quiz_name = []
                    quiz_lst = []
                    quizs = bs.select('#region-main > div > table > tbody > tr > td.cell.c1 > a')
                    
                    for quiz in quizs:
                        quiz_lst.append(str(quiz))
                        quiz_name.append(quiz.get_text())
                    
                    quiz_deadline_lst = []
                    quiz_deadlines = bs.select('#region-main > div > table > tbody > tr > td.cell.c2')
                    for d in quiz_deadlines:
                        quiz_deadline_lst.append(d.get_text())

                    quiz_id_lst = []
                    quiz_url_lst = []
                    quiz_status_lst = []
                    
                    # (int형) id만 quiz_id_lst에 담음
                    for i in quiz_lst:
                        index = i.find('id')
                        quiz_id_lst.append(int(i[index+3:index+9]))
                    #print(quiz_id_lst)

                    # 반복되는 링크와 id를 합쳐 퀴즈 url 리스트를 생성
                    cnt = len(quiz_id_lst)
                    for i in range(cnt):
                        quiz_url_lst.append('https://ecampus.smu.ac.kr/mod/quiz/view.php?id='+str(quiz_id_lst[i]))
                    #print(quiz_url_lst)
                    
                    # 퀴즈 답안 제출 확인
                    if (request5.status_code == 200):
                        for i in range(cnt):
                            #print(quiz_name[i])
                            request3 = s.post(quiz_url_lst[i])
                            bs = BeautifulSoup(request3.text, 'html.parser')
                            t = bs.select('#region-main > div > h3')
                            # 퀴즈 미제출 시 빈 리스트가 반환되는 것을 확인 -> 빈 리스트인 경우 '미제출' 출력
                            if t:
                                quiz_status_lst.append('제출 완료')
                            else:
                                quiz_status_lst.append('미제출')
                                        
                    i += 1

                    size = len(quiz_name)
                    absent = '미제출'
                    unsubmit_lst = []
                    value3 = ''
                        
                    for i in range(0, size):
                        if absent in quiz_status_lst[i]:
                            string = quiz_name[i] + ' / 현황: ' + quiz_status_lst[i] + ' / 마감일: ' + quiz_deadline_lst[i]
                            unsubmit_lst.append(string)
                    
                    if absent not in quiz_status_lst:
                        value3_lst.append('모두 제출 완료!!')
                    elif absent in quiz_status_lst:
                        for i in unsubmit_lst:
                            value3 += (i + '\n')
                        value3_lst.append(value3)
            embed3 = discord.Embed(title = '미제출 퀴즈 목록', description = '(2021학년도 2학기)', color = 0xBDECB6)
            for i in range(count):
                embed3.add_field(name = class_name_lst[i], value = value3_lst[i], inline = False)
            await message.channel.send(embed = embed3)

client.run(token)
