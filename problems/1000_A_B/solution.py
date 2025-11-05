"""
BOJ 1000 - A+B
"""

import sys


def read_input():
    """입력을 읽어서 반환"""
    return sys.stdin.readline().rstrip()


def write_output(output_data):
    """출력 데이터를 출력"""
    print(output_data)


def solve(input_data):
    # 여기에 풀이 로직만 작성
    a = int(input_data.split()[0])
    b = int(input_data.split()[1])
    return a+b


if __name__ == "__main__":
    input_data = read_input()
    output_data = solve(input_data)
    write_output(output_data)
