"""
BOJ 21394 - 숫자 카드
"""

import sys
from collections import deque

def read_input():
    """입력을 읽어서 반환"""
    t = int(sys.stdin.readline())
    input_data = []
    for i in range(t):
        line = list(map(int, sys.stdin.readline().rstrip().split()))
        input_data.append(line)
    return input_data


def write_output(output_data):
    """출력 데이터를 출력"""
    for data in output_data:
        print(' '.join(map(str, data)))


def solve(input_data):
    # 여기에 풀이 로직만 작성
    output_data = []

    for data in input_data:
        num = []
        for i in range(9):
            for j in range(data[i]):
                card = i + 1
                if card == 6:
                    num.append(9)
                else:
                    num.append(card)

        num.sort(reverse=True)
        origin = deque()

        for i in reversed(range(len(num))):
            n = num.pop()

            if i % 2 == 0:
                origin.appendleft(n)
            else:
                origin.append(n)

        output_data.append(origin)

    return output_data


if __name__ == "__main__":
    input_data = read_input()
    output_data = solve(input_data)
    write_output(output_data)
