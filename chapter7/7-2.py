## closure.py
# class Mul:
    # def __init__(self, m):
#         self.m = m
# # 
    # def __call__(self, n):
        # return self.m * n
# 
# if __name__ == "__main__":
    # mul3 = Mul(3)
    # mul5 = Mul(5)
# 
# print(mul3(10))  # 30 출력
# print(mul5(10))  # 50 출력

def mul(m):
    def wrapper(n):
        return m * n
    return wrapper

if __name__ == "__main__":
    mul3 = mul(3)
    mul5 = mul(5)

    print(mul3(10))  # 30 출력
    print(mul5(10))  # 50 출력