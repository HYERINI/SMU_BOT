# 로그인 페이지 스크레이핑

import requests
from bs4 import BeautifulSoup

session = requests.session()
url = "https://ecampus.smu.ac.kr/login.php"

user_info = {
    "return_url":"https://ecampus.smu.ac.kr/",
    "username":"학번",
    "password":"비밀번호"
}
response = session.post(url, data = user_info)

response.raise_for_status()

url = "https://ecampus.smu.ac.kr/"
response = session.get(url)
response.raise_for_status()

bs = BeautifulSoup(response.text, "html.parser")
print(bs)