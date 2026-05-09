# thread_test.py
import time

def long_task():  # 5초의 시간이 걸리는 함수
    for i in range(5):
        time.sleep(1)  # 1초간 대기한다.
        print(f"working:{i}\n")

print("Start")

for i in range(5):  # long_task를 5회 수행한다.
    long_task()

print("End")