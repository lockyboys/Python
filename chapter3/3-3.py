# test_list = ['one', 'two', 'three'] 
# for i in test_list: 
    # print(i)

# a = [(1,2), (3,4), (5,6)]
# for (first, last) in a: print(first + last)

# a = [(1,2), (3,4), (5,6)]
# for total in a: print(total)

# marks1.py
# marks = [90, 25, 67, 45, 80]   # 학생들의 시험 점수 리스트
# 
# number = 0   # 학생에게 붙여 줄 번호
# for mark in marks:   # 90, 25, 67, 45, 80을 순서대로 mark에 대입
    # number += 1 
    # if mark >= 60: 
        # print(f"{number}번 학생은 합격입니다.")
    # else: 
        # print(f"{number}번 학생은 불합격입니다.")

# marks1.py
# marks = [90, 25, 67, 45, 80]   # 학생들의 시험 점수 리스트

# number = 0   # 학생에게 붙여 줄 번호
# for mark in marks:   # 90, 25, 67, 45, 80을 순서대로 mark에 대입
    # number += 1 
    # if mark >= 60: 
        # print("%d번 학생은 합격입니다." % number)
    # else: 
        # print("%d번 학생은 불합격입니다." % number)

# a = [(1,90), (2,25), (3,67), (4,45), (5,80)]
# for (number, mark) in a: 
    # if mark >= 60: 
        # print("%d번 학생은 합격입니다." % number)
    # else: 
        # print("%d번 학생은 불합격입니다." % number)

# for i in range(2,10):        # 1번 for문
    # for j in range(1, 10):   # 2번 for문
        # f = i * j
        # print("%d X %d = "{0:0>2}".format(f)" % i % j  , end="  ") 
        # print('') 

# python 
for i in range(2, 10): 
    for j in range(1, 10): 
        # f = i * j 
        print(f"{i} X {j} = {i*j:02d}", end="  ") 
    print('\t')
print('\a')