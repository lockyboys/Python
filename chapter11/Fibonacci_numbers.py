sum_even = 0

a = 1
b = 2

while b <= 4000000:
    if b % 2 == 0:
        sum_even += b
    
    a, b = b, a + b

print(sum_even, b)

#Fibonacci numbers gcc 스타일로 짬.
a = 1
b = 2
sum = 0

while b <= 4000000:
    #짝수 인지 확인
    if (b % 2) == 0:
        sum += b
    next = a + b

    # 값 이동
    a = b
    b = next

print("%d  %d\n" % (sum, next))