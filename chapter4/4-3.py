# newfile2.py
# f = open("C:/python/새파일1.txt", 'w', encoding="utf-8")
# f.close()

f = open("C:/python/새파일.txt", 'w', encoding="utf-8")
for i in range(1, 11):
    data = f"{i: 3d}번째 줄입니다.\n"
    f.write(data)
f.close()

# readline_test.py
# f = open("C:/python/새파일.txt", 'r')
# line = f.readline()
# print(line)
# f.close()

# readline_all.py
# f = open("C:/python/새파일.txt", 'r')
# while True:
    # line = f.readline()
    # if not line: break
    # print(line, end=' ')
# f.close()

# readlines.py
# f = open("C:/python/새파일.txt", 'r')
# lines = f.readlines()
# for line in lines:
    # print(line, end=' ')
# f.close()

# f = open("C:/python/새파일.txt", 'r')
# lines = f.readlines()
# for line in lines:
    # line = line.rstrip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
    # print(line)
# f.close()


# f = open("C:/python/새파일.txt", 'r')
# lines = f.readlines()
# for line in lines:
    # line = line.replace('\n','')  # 줄 끝의 줄 바꿈 문자를 제거한다.
    # print(line)
# f.close()

'''
read 함수 사용하기
세 번째는 read 함수를 사용하는 방법이다. 다음 예를 살펴보자.
'''
# read.py
# f = open("C:/python/새파일.txt", 'r')
# data = f.read()
# print(data)
# f.close()

'''
파일 객체를 for 문과 함께 사용하기
네 번째는 파일 객체를 for 문과 함께 사용하는 방법이다.
'''

# read_for.py
# f = open("C:/python/새파일.txt", 'r')
# for line in f:
    # print(line)
# f.close()

'''
파일에 새로운 내용 추가하기
쓰기 모드('w')로 파일을 열 때 이미 존재하는 파일을 열면 그 파일의 내용이 모두 사라진다. 하지만 원래 있던 값을 유지하면서 새로운 값만 추가해야 할 경우도 있다. 이런 경우에는 파일을 추가 모드('a')로 열면 된다. IDLE 에디터로 다음 코드를 작성해 보자.
'''


# add_data.py
f = open("C:/python/새파일.txt",'a')
for i in range(11, 20):
    data = f"{i}번째 줄입니다.\n"
    f.write(data)
f.close()