from bs4.element import NavigableString
import requests
from bs4 import BeautifulSoup

login_url = 'https://ecampus.smu.ac.kr/login/index.php'
class_url = 'https://ecampus.smu.ac.kr/?'
class1_url = 'https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id=64597'

user_info = {
    'username':'학번',
    'password':'비밀번호'
}

with requests.Session() as s:
    request = s.post(login_url, data = user_info)
    request2 = s.post(class1_url, data = user_info)
    if (request.status_code == 200):
        bs = BeautifulSoup(request2.text, 'html.parser')

lecture_name = bs.find_all("td", {"class", "text-left"})
name_lst = []
for name in lecture_name:
    name_lst.append(name.text.strip())
name_lst = name_lst[3:]
print(name_lst)

rates = bs.find_all("td", {"class", "text-center"})
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

deadlines = bs.find_all('h3', {'class', 'modal-title'})
deadline_lst = []
for deadline in deadlines:
    print(deadline)