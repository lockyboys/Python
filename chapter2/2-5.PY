# a = [1, 2, 3]
# print(id(a))
# from copy import copy
a = [1, 2, 3]
# b = copy(a)
# b = a
# print(b)
# a = [1, 2, 3]
# b = a.copy()
# Print(b is a)
# False
# b is a
a, b = ('python', 'life')
print(a)
print(b)
dic = {'name': 'pey', 'phone': '010-9999-1234', 'birth': '1118'}
print(type(dic))
a = {'name': 'pey', 'phone': '010-9999-1234', 'birth': '1118'}

for k in a.keys():
    print(k)
for t in a.values():
    print(t)
for t in a.items():
    print(t)
a = {'name': 'pey', 'phone': '010-9999-1234', 'birth': '1118'}
print('name' in a)