# 강좌 목록 스크레이핑

import requests
from bs4 import BeautifulSoup

login_url = 'https://ecampus.smu.ac.kr/login/index.php'

user_info = {
    'username':'학번',
    'password':'비밀번호'
}

with requests.Session() as s:
    request = s.post(login_url, data = user_info)
    if (request.status_code == 200):
        bs = BeautifulSoup(request.text, 'html.parser')

lectures = bs.select("#region-main > div > div.progress_courses > div > ul > li > div > a > div.course-name > div.course-title > h3")
for lecture in lectures:
    print(lecture.text)