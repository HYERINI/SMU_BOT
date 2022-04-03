import requests
from bs4 import BeautifulSoup

login_url = 'https://ecampus.smu.ac.kr/login/index.php'  #로그인 창 주소
class2021_url = 'https://ecampus.smu.ac.kr/local/ubion/user/?year=2021&semester=20'  #강의 인덱스 가져오기 위한 주소

lst2 = []   # 각 과목별 퀴즈 url

user_info = {
    'username':'학번',
    'password':'비밀번호'
}

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

    print('---------------------퀴즈 제출 현황---------------------------------')
    print(count)
    print(len(class_name_lst))
    # 퀴즈 제출 현황 크롤링
    if (request3.status_code == 200):
        for i in range(count):
            print(class_name_lst[i])
            request5 = s.post(lst2[i])
            bs = BeautifulSoup(request5.text, 'html.parser')

            # 퀴즈 url 리스트(quiz_url_lst) 만들기
            if (request.status_code == 200):
                bs = BeautifulSoup(request5.text, 'html.parser')

                quiz_name = []
                quiz_lst = []
                quizs = bs.select('#region-main > div > table > tbody > tr > td.cell.c1 > a')

                # 퀴즈마다 부여된 고유 id 추출
                for quiz in quizs:
                    quiz_lst.append(str(quiz))
                    quiz_name.append(quiz.get_text())

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
            print('총 개수: ' + str(cnt))
            
            # 퀴즈 답안 제출 확인
            if (request5.status_code == 200):
                for i in range(cnt):
                    print(quiz_name[i])
                    request3 = s.post(quiz_url_lst[i])
                    status_lst = []
                    bs = BeautifulSoup(request3.text, 'html.parser')
                    t = bs.select('#region-main > div > h3')
                    # 퀴즈 미제출 시 빈 리스트가 반환되는 것을 확인 -> 빈 리스트인 경우 '미제출' 출력
                    if t:
                        print('제출 완료')
                    else:
                        print('미제출')
                print('---------------------------------------------------')
            

