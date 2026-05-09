# def add2(a, b):
    # return a+b

# def say():
    # return 'Hi'
# 
# def add(a, b): 
    # print(f"{a}, {b}의 합은 {a+b}입니다.")
# 
# def say2(): 
    # print('hi')

# def sub(a, b):
    # return a - b

#  def add_many(*args): 
    # result = 0 
    # for i in args: 
        # result = result + i   # *args에 입력받은 모든 값을 더한다.
    # return result 

# result = sub(a=7, b=3)  # a에 7, b에 3을 전달
# print(result)
# result = sub(b=5, a=3)  # b에 5, a에 3을 전달
# print(result)
# c = add(3,4)
# print(c)
# d = say2()
# print(c)
# print(say())
# print(add2(3,4))

# def add_mul(choice, *args): 
    # if choice == "add":   # 매개변수 choice에 "add"를 입력받았을 때
        # result = 0 
        # for i in args: 
            # result = result + i 
    # elif choice == "mul":   # 매개변수 choice에 "mul"을 입력받았을 때
        # result = 1 
        # for i in args: 
            # result = result * i 
    # return result 

# result = add_mul('add', 1,2,3,4,5)
# print(result)
# 15
# result = add_mul('mul', 1,2,3,4,5)
# print(result)


# def print_kwargs(**kwargs):
    # print(kwargs)

# print_kwargs(a=1)
# {'a': 1}
# print_kwargs(name='foo', age=3)
# {'name': 'foo', 'age': 3}
# print_kwargs(name='홍길동', age=25, city='서울', job='개발자')
# {'name': '홍길동', 'age': 25, 'city': '서울', 'job': '개발자'}

# vartest.py
# a = 1
# def vartest(a):
    # a = a +1

# vartest(a)
# print(a)

# vartest_return.py
# a = 1 
# def vartest(a): 
    # a = a +1 
    # return a

# a = vartest(a) 
# print(a)

# vartest_global.py
a = 1 
# def vartest(): 
    # global a 
    # a = a+1

# vartest() 
# print(a)

# def change_list(my_list):
    # my_list.append(4)  # 리스트에 값을 추가
    # print(id(my_list))
# a = [1, 2, 3]
# print(id(a))
# change_list(a)
# print(a)
# [1, 2, 3, 4]

# vartest_global.py
# b = [1,2,3,4] 
# def vartest(b): 
    # b = b.append(5)

# vartest(b) 
# print(b)

# vartest_global.py
# b = {'name': '홍길동', 'age': 53, 'city': '과천', 'job': '개발자', 'email' : 'jeajea.park@gmail.com'} # {1,2,3,4} 
# def vartest(b): 
    # b = b.pop('email')
    # return b
# 
# a=vartest(b) 
# print(a)
# print(b)
# 
# add = lambda a, b: a+b
# # result = add(3, 4)
# print(result)
# 
# a = [lambda a, b: a+b, lambda a, b: a*b]
# 
# print(a[1](3,4))

def add(a, b):
    """
    두 숫자를 더하는 함수

    Parameters:
    a (int, float): 첫 번째 숫자
    b (int, float): 두 번째 숫자

    Returns:
    int, float: 두 숫자의 합
    """
    return a + b

# 독스트링 확인하기
print(add.__doc__)
add.__doc__