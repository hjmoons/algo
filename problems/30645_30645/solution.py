"""
BOJ 30645 - 인형 전시
"""

import sys


def read_input():
    """입력을 읽어서 반환"""
    r, c = map(int, sys.stdin.readline().rstrip().split())
    n = int(sys.stdin.readline().rstrip())
    h = list(map(int, sys.stdin.readline().rstrip().split()))
    return r, c, n, h


def write_output(output_data):
    """출력 데이터를 출력"""
    print(output_data)


def solve(r, c, n, h):
    max = r * c
    dolls = {}
    output_data = 0

    for i in range(n):
        if dolls.get(h[i]) == None:
            dolls[h[i]] = 1
        else:
            dolls[h[i]] += 1
    
    for i in dolls.keys():
        if dolls[i] > c:
            output_data += c
        else:
            output_data += dolls[i]
        
        if output_data >= max:
            output_data = max
            break

    return output_data


if __name__ == "__main__":
    r, c, n, h = read_input()
    output_data = solve(r, c, n, h)
    write_output(output_data)
