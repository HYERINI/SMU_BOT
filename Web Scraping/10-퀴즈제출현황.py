import requests
from bs4 import BeautifulSoup

login_url = 'https://ecampus.smu.ac.kr/login/index.php'
quiz_url = 'https://ecampus.smu.ac.kr/mod/quiz/index.php?id=64600'

user_info = {
    'username':'학번',
    'password':'비밀번호'
}

with requests.Session() as s:
    request = s.post(login_url, data = user_info)
    request2 = s.post(quiz_url, data = user_info)
    
    # 퀴즈 url 리스트(quiz_url_lst) 만들기
    if (request.status_code == 200):
        bs = BeautifulSoup(request2.text, 'html.parser')

        quiz_lst = []
        quizs = bs.select('#region-main > div > table > tbody > tr > td.cell.c1 > a')

        # 퀴즈마다 부여된 고유 id 추출
        for quiz in quizs:
            quiz_lst.append(str(quiz))
        print(quiz.get_text())

        quiz_id_lst = []
        quiz_url_lst = []

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
    print(cnt)
    
    # 퀴즈 답안 제출 확인
    if (request2.status_code == 200):
        for i in range(cnt):
            request3 = s.post(quiz_url_lst[i])
            bs = BeautifulSoup(request3.text, 'html.parser')
            t = bs.select('#region-main > div > h3')
            # 퀴즈 미제출 시 빈 리스트가 반환되는 것을 확인 -> 빈 리스트인 경우 '미제출' 출력
            if t:
                print('제출 완료')
            else:
                print('미제출')