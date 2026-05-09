class FourCal:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    
    def setdata(self, first, second):
        self.first = first
        self.second = second

    def add(self):
        result = self.first + self.second
        return result
    def mul(self):
        result = self.first * self.second
        return result
    def sub(self):
        result = self.first - self.second
        return result
    def div(self):
        result = self.first / self.second
        return result
    
class MoreFourCal(FourCal):
    def pow(self):
        result = self.first ** self.second
        return result

class SafeFourCal(FourCal):
    def div(self):
        if self.second == 0:  # 나누는 값이 0인 경우 0을 반환하도록 수정
            return 0
        else:
            return self.first / self.second

a = SafeFourCal(4, 0)
x = MoreFourCal(4, 0)
# print(a.pow())
print(a.div())
print(x.div())

# a = FourCal()
# b = FourCal()

# a.setdata(4, 2)
# b.setdata(1, 3)

# print(type(a))

# print(a.first)
# print(a.second)

# print(b.first)
# print(b.second)

# print(a.add())
# print(a.mul())
# print(a.sub())
# print(a.div())

# print(b.add())
# print(b.mul())
# print(b.div())
# print(b.sub())