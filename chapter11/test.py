import math

def solution(signals):
    # 1. 모든 신호등의 주기를 계산하고, 탐색할 최대 범위를 정합니다.
    # 각 주기(L)들의 최소공배수(LCM)를 구하면 더 정확하지만, 
    # 문제 제한 사항이 작으므로 1,000,000 정도면 충분합니다.

    # 참고: LCM을 구하는 법
    lcm = 1
    for g, y, r in signals:
        cycle = g + y + r
        gcd_value = math.gcd(lcm, cycle)
        lcm = (lcm * cycle) // math.gcd(lcm, cycle)
    
    return lcm

if __name__ == "__main__":

    _signals = [
        [ 2, 1, 2], #{"초록불": 2, "노랑불": 1, "빨강불": 2},
        [ 5, 1, 1]  #{"초록불": 5, "노랑불": 1, "빨강불": 1}
    ]

    result = solution(_signals)
    print(result)