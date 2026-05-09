# a = "Life is too short"
# b = a.encode('utf-8')
# 
# print(b)

# a= "한글"
# b = a.encode("ascii")
# print(b)

a = '한글'
b = a.encode('euc-kr')
print(b)
print(b.decode('euc-kr'))
# b'\xc7\xd1\xb1\xdb'
b = a.encode('utf-8')
print(b.decode('utf-8'))
print(b)