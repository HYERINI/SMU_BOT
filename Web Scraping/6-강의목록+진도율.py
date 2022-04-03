import requests
from bs4 import BeautifulSoup

login_url = 'https://ecampus.smu.ac.kr/login/index.php'
class_url = 'https://ecampus.smu.ac.kr/?'
class1_url = 'https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id=64600'

user_info = {
    'username':'학번',
    'password':'비밀번호'
}

with requests.Session() as s:
    request = s.post(login_url, data = user_info)
    request2 = s.post(class1_url, data = user_info)
    if (request.status_code == 200):
        bs = BeautifulSoup(request2.text, 'html.parser')
        lecture_name = bs.find_all('td', {'class', 'text-left'})
        rates = bs.find_all('td', {'class', 'text-center'})

# 강의 목록
name_lst = []
for name in lecture_name:
    name_lst.append(name.text.strip())
name_lst = name_lst[3:] # 인덱스 0~2번은 학생 개인 정보
print(name_lst)
print(len(name_lst))

# 진도율
rate_list = []
for rate in rates:
    rate_list.append(str(rate.text))
a_li = []
for word in rate_list:
    if '%' in word:         # 진도율만 뽑아내기 위해서 %가 포함된 부분만 검색
        a_li.append(word)
    elif word == '-':
        a_li.append(word)
print(a_li)
print(len(a_li))

# 한 눈에 보기
size = len(name_lst)
print("현재까지 업로드 된 강의 수:", size)
for i in range(0, size):
    print('강의 제목 : ' + name_lst[i], '-> 강의 진도율 : ' + a_li[i])
