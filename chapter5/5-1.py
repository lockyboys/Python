# calculator.py
# result = 0

# def add(num):
    # global result
    # result += num  # 결괏값(result)에 입력값(num) 더하기
    # return result  # 결괏값 반환

# print(add(3))
# print(add(4))

# calculator2.py
result1 = 0
result2 = 0

def add1(num):  # 계산기1
    global result1
    result1 += num
    return result1

def add2(num):  # 계산기2
    global result2
    result2 += num
    return result2

print(add1(3))
print(add1(4))
print(add2(3))
print(add2(7))
