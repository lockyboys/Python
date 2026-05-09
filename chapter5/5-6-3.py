from faker import Faker

# 기본 영어 데이터
# fake = Faker()
# print(fake.name())

# 한국어 데이터
fake_ko = Faker('ko-KR')
# print(fake_ko.name())

# print(fake.address())
# print(fake_ko.address())
print(divmod(2,2))
test_data = [(fake_ko.name(), fake_ko.address(), fake_ko.text()) for i in range(30)]
a = 0
for i in test_data:
    a += 1
    if (a % 10) == 0:
        i = input()
        print(i)
    print(a,i)