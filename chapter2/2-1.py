# a = 3
# b = 4
# a + b
# b = a * b
# b = a / b
'''
** 연산자는 a ** b처럼 사용하면
a의 b제곱 값을 반환
'''
# b = a ** b
'''
나머지를 반환 한다
'''
b = 7 % 3
print(b)
b = 3 % 7
print(b)
'''
몫을 반환 한다
'''
# b = 7 // 4
# b = 1
"""
a = a + 1은 
다음과 같이 간략하게 표현할 수 있다.
"""
# b += 1

# b = 1
"""
a = a - 1과 같음
"""
# b -= 1  
b = 2
'''
복합 연산자에는 다음과 같은 것들이 있다.
+=, -=, *=, /=, //=, %=, **=
'''
# a = a * 3과 같음
# b *= 3  
# print(b)
# print(type(b))
# print(b)

# a = "I eat %d apples." % 4
# print(a)
# 'I eat 3 apples.'

# b = "I eat %s apples." % "five"
# print(b)
# 'I eat five apples.'

# number = 10
# day = "three"
# a = "I ate %d apples. so I was sick for %s days." % (number, day)
# print(a)
# 'I ate 10 apples. so I was sick for three days.

# a = "%-10s" % "hi"
# print(a)
# '        hi'


# a = "%5.3f" % 2343.42134234
# print(a)
# '3.4213'

# a = "I ate {0} apples. so I was sick for {day} days.".format(10, day=3)
# print(a)
# 'I ate 10 apples. so I was sick for 3 days.'

# a = "{0:<10}".format("hi")
# print(a)
# 'hi        '
# :<10 표현식을 사용하면 치환되는 문자열을 왼쪽으로 정렬하고 문자열의 총 자릿수를 10으로 맞출 수 있다.

# 오른쪽 정렬
# a = "{0:>10}".format("hi")
# print(a)
# '        hi'
# 오른쪽 정렬은 :< 대신 :>을 사용하면 된다. 화살표의 방향을 생각하면 어느 쪽으로 정렬되는지 바로 알 수 있다.

# 가운데 정렬
# a = "{0:^10}".format("hi")
# print(a)
# '    hi    '

# 가운데 정렬
a = "{0:*^10}".format("hi")
print(a)
# '    hi    '