"""
BOJ 16401 - 과자 나눠주기
"""

import sys


def read_input():
    """입력을 읽어서 반환"""
    m, n = map(int, sys.stdin.readline().rstrip().split())
    l = list(map(int, sys.stdin.readline().rstrip().split()))
    return m, n, l


def write_output(output_data):
    """출력 데이터를 출력"""
    print(output_data)


def solve(m, n, l):
    first = 1
    last = max(l)
    answer = 0

    while first <= last:
        mid = int((first + last) / 2)
        sum = 0
        for snack in l:
            sum += int(snack / mid)
        if sum >= m:
            answer = mid
            first = mid + 1
        else:
            last = mid - 1
        
    return answer

if __name__ == "__main__":
    m, n, l = read_input()
    output_data = solve(m, n, l)
    write_output(output_data)
