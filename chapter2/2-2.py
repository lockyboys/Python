# a = "Life is too short, You need Python"
# b = "a"
# c = "123"
# print(type(a))
# a = """Life is \"too\" \\ short, \'You need Python"""
# print(a)
# head = "Python"
# tail = " is fun!"
# print(head + tail)
# 'Python is fun!'

# multistring.py
# print("=" * 50)
# print("My Program")
# print("=" * 50)

# a = "Life is too short"
# print(len(a))


'''
a[   :    :   ]
  이상 미만 간격
'''
# a = "Life is too short, You need Python"
# b= a[::10]
# print(b)
# c= a[::-2]
# print(c)

# a = "Life is too short, You need Python"
# print(a[3])
# print(a[0])
# 'L'
# print(a[12])
# 's'
# print(a[-1])
# 'n'
# print(a[-3])
# print(a[-0])

# a = "Life is too short, You need Python"
# b = a[0] + a[1] + a[2] + a[3]
# print(b)
# 'Life'

# a = "20230331Rainy"
# date = a[:8]
# weather = a[8:]
# print(date)
# '20230331'
# print(weather)
# 'Rainy'

# a = "Pithon"
# print(a[:1])
# 'P'
# print(a[2:])
# 'thon'
# print(a[:1] + 'y' + a[2:])

a = " hi my name is p ark "
print(a.strip())