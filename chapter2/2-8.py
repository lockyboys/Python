# a = [1, 2, 3]
# b = a
# print(id(a))
# print(id(b))
# a[1]=4
# print(a)
# print(b)

a = [1, 2, 3]
b = a[:]
a[1]=4
print(a)
print(b)
print(id(a))
print(id(b))

a = 3
b = 5
a, b = b, a
print(a)
print(b)