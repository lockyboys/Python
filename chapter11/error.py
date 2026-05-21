import math

def solution(signals):
    # 1. 모든 신호등의 주기를 계산하고, 탐색할 최대 범위를 정합니다.
    # 각 주기(L)들의 최소공배수(LCM)를 구하면 더 정확하지만, 
    # 문제 제한 사항이 작으므로 1,000,000 정도면 충분합니다.

    # 참고: LCM을 구하는 법
    lcm = 1
    for g, y, r in signals:
        cycle = g + y + r
        lcm = (lcm * cycle) // math.gcd(lcm, cycle)

    # 2. 1초부터 최소공배수 시간까지 시뮬레이션
    for t in range(1, lcm + 1):
        is_all_yellow = True

        for g, y, r in signals:
            cycle_length = g + y + r
            # 현재 시각 t에서의 상대적 위치
            current_pos = (t - 1) % cycle_length

            # 노란불 구간인지 확인: G초 이후부터 (G+Y)초 이전까지
            if not (g <= current_pos < g + y):
                is_all_yellow = False
                break

        # 모든 신호등이 노란불이라면 해당 시각 반환
        if is_all_yellow:
            return t

    # 탐색 종료 시까지 찾지 못하면 -1
    return -1

if __name__ == "__main__":

    _signals = [
        [ 1, 1, 4], #{"초록불": 2, "노랑불": 1, "빨강불": 2},
        [ 2, 1, 3],  #{"초록불": 5, "노랑불": 1, "빨강불": 1}
        [ 3, 1, 2],
        [ 4, 1, 1]
    ]
    
    result = solution(_signals)
    print(result)