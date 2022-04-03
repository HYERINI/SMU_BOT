from bs4.element import NavigableString
import requests
from bs4 import BeautifulSoup

login_url = 'https://ecampus.smu.ac.kr/login/index.php'
class2021_url = 'https://ecampus.smu.ac.kr/local/ubion/user/?year=2021&semester=20'

url_lst = []

user_info = {
    'username':'학번    ',
    'password':'비밀번호'
}
total_name = []
with requests.Session() as s:
    request = s.post(login_url, data = user_info)
    request2 = s.post(class2021_url, data = user_info)
    if (request.status_code == 200):
        bs = BeautifulSoup(request2.text, 'html.parser')

        lectures = bs.select('#region-main > div > div > div.course_lists > div > table > tbody > tr > td > div > a')

        class_list = []
        for lecture in lectures:
            class_list.append(str(lecture))
        lst = []
        for i in class_list:
            index = i.find('id')
            lst.append(int(i[index+3:index+8]))
        # print(lst)         //강의의 코드번호 추출
        count = len(lst)
        for i in range(count):
            url_lst.append('https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id='+str(lst[i]))

    if (request2.status_code == 200):
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
                    a_li.append(word)
            
            size = len(a_li)

            for i in range(0, size): {
                print('강의 제목 : ' + name_lst[i], '-> 강의 진도율 : ' + a_li[i])
            }
            print()