import requests
from bs4 import BeautifulSoup

login_url = 'https://ecampus.smu.ac.kr/login/index.php'  #로그인 창 주소
class2021_url = 'https://ecampus.smu.ac.kr/local/ubion/user/?year=2021&semester=20'  #강의 인덱스 가져오기 위한 주소
url_lst = []
url_lst_assign = []


user_info = {
    'username':'학번',
    'password':'비밀번호'
}

with requests.Session() as s:
    #필요한 주소들 & selector들 미리 설정
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


    print("--------------------------------강의 진도 현황-------------------------------------------\n")

    #강의진도현황크롤링하기
    if (request3.status_code == 200):
        for i in range(count):
            request3 = s.post(url_lst[i])
            name_lst = []
            rate_list = []
            a_li = []
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
                    a_li.append('0%')
            
            size = len(a_li)

            print(class_name_lst[i] + '\n')
            i += 1
            for i in range(0, size): 
                print('강의 제목 : ' + name_lst[i] + '-> 강의 진도율 : ' + a_li[i])
            print('-----------------------------------------------------------------------------------------\n')
            
            print('\n')            

    #과제제출현황크롤링하기
    print("--------------------------------과제 제출 현황-------------------------------------------\n")

    if (request.status_code == 200):
        for i in range(count):
            request4 = s.post(url_lst_assign[i])

            bs = BeautifulSoup(request4.text, 'html.parser')
            assignment_name = bs.find_all("td", {"class", "cell c1"})
            assignment_rates = bs.find_all("td", {"class", "cell c3"})
            assignment_close = bs.find_all("td", {"class", "cell c2"})

            assignment_name_lst = []
            for name in assignment_name:
                assignment_name_lst.append(name.text.strip())

            assignment_rate_lst = []
            for rate in assignment_rates:
                assignment_rate_lst.append(rate.text.strip())

            assignment_close_lst = []
            for close in assignment_close:
                assignment_close_lst.append(close.text.strip())

            size = len(assignment_name_lst)
            print(class_name_lst[i] + '\n')
            i += 1
            for i in range(0, size):
                print('과제 제목 : ' + assignment_name_lst[i], '\n과제 현황 : ' + assignment_rate_lst[i])
                print('마감 기한 : ' + assignment_close_lst[i] + '\n')
            print('-----------------------------------------------------------------------------------------\n')

    # 강의별 퀴즈 url id 추출
    if (request.status_code == 200):
        bs = BeautifulSoup(request3.text, 'html.parser')

        lectures = bs.select('#region-main > div > div > div.course_lists > div > table > tbody > tr > td > div > a')

        lst2 = []
        for i in class_list:
            index = i.find('id')
            lst.append(int(i[index+3:index+8]))
        count = len(lst)
        for i in range(count):
            lst2.append('https://ecampus.smu.ac.kr/mod/quiz/index.php?id='+str(lst[i]))

    print('---------------------퀴즈 제출 현황---------------------------------')

    # 퀴즈 제출 현황 크롤링
    if (request3.status_code == 200):
        count2 = len(class_name_lst)
        for i in range(count2):
            print(class_name_lst[i])
            request5 = s.post(lst2[i])
            bs = BeautifulSoup(request5.text, 'html.parser')

            # 퀴즈 url 리스트(quiz_url_lst) 만들기
            if (request5.status_code == 200):
                bs = BeautifulSoup(request5.text, 'html.parser')

                quiz_name = []
                quiz_lst = []
                quizs = bs.select('#region-main > div > table > tbody > tr > td.cell.c1 > a')

                # 퀴즈마다 부여된 고유 id 추출
                for quiz in quizs:
                    quiz_lst.append(str(quiz))
                    quiz_name.append(quiz.get_text())

                quiz_deadline_lst = []
                quiz_deadlines = bs.select('#region-main > div > table > tbody > tr > td.cell.c2')
                for d in quiz_deadlines:
                    quiz_deadline_lst.append(d.get_text())
        
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
                    print(quiz_deadline_lst[i])
                print('---------------------------------------------------')