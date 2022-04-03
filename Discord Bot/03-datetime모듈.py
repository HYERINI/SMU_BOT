import datetime as dt

current_time = dt.datetime.now()
print(current_time.strftime('%Y-%m-%d %H:%M:%S'))

# 문자열로부터 날짜 뽑아내기
deadline_time_str = '2021-07-31 23:59:00'
deadline_time = dt.datetime.strptime(deadline_time_str, "%Y-%m-%d %H:%M:%S")

print(deadline_time)

# 현재시간 - 예전시간
current_date = current_time.date()
deadline_date = deadline_time.date()

difference = (deadline_date - current_date).days

print(difference)

if difference > 0:
    print("수강 가능 기간이 지났습니다.")
else:
    print(-difference, "/ 빠른 시간 내에 수강해주세요.")