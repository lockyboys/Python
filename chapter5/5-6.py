# webbrowser.open_new('http://python.org')
# import time
# import threading
# 
# def long_task():
    # for i in range(5):
        # time.sleep(1)
        # print(f"working:{i}\n")
# 
# print("Start")
# 
# threads = []
# for i in range(5):
    # t = threading.Thread(target=long_task)
    # threads.append(t)
# 
# for t in threads:
    # t.start()
# 
# for t in threads:
    # t.join()  # join으로 스레드가 종료될때까지 기다린다.
# 
# print("End")
# 
# if __name__ == "__main__":
#   print("????End!!!!")
# 
# 
  # webbrowser_test.py
# import webbrowser
# 
# webbrowser.open_new('http://python.org')
# 
# thread_test.py
# import webbrowser
# webbrowser.open('http://python.org')
from faker import Faker
fake = Faker()
fake.name()
fake = Faker('ko-KR')
a = fake.name()
print(a)
# import os
# print(os.environ['PATH'])