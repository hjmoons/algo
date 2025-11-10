"""
BOJ 1411 - 비슷한 단어
"""

import sys


def read_input():
    """입력을 읽어서 반환"""
    n = int(sys.stdin.readline().rstrip())
    input_data = []
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        input_data.append(line.rstrip())
    return n, input_data


def write_output(output_data):
    """출력 데이터를 출력"""
    print(output_data)


def solve(n, input_data):
    # 여기에 풀이 로직만 작성
    output_data = 0

    for i in range(n):
        for j in range(i+1, n):
            alpha = {}
            bet = {}
            check = True

            for k in range(len(input_data[i])):
                if alpha.get(input_data[i][k]) == input_data[j][k] and bet.get(input_data[j][k]) == input_data[i][k]:
                    continue
                elif alpha.get(input_data[i][k]) == None and bet.get(input_data[j][k]) == None:
                    alpha[input_data[i][k]] = input_data[j][k]
                    bet[input_data[j][k]] = input_data[i][k]
                else:
                    check = False
                    break
                
            if check:
                output_data = output_data + 1

    return output_data


# ========== 최적화 코드 ==========
# def solve(n, input_data):
#     """
#     최적화 아이디어:
#     1. 패턴 해싱: 각 단어를 패턴으로 변환하여 O(1)에 비교
#        예: "aabbcc" -> "112233", "ddeeff" -> "112233" (같은 패턴)
#
#     2. 패턴 생성 방식:
#        - 각 문자가 처음 등장한 순서대로 번호 부여
#        - 예: "abca" -> "0120" (a=0, b=1, c=2, a는 이미 0)
#
#     3. 같은 패턴을 가진 단어끼리만 비슷한 단어
#
#     시간복잡도: O(N^2 * L) -> O(N * L + N^2)
#     """
#     from collections import defaultdict
#
#     def get_pattern(word):
#         """단어를 패턴 문자열로 변환"""
#         char_map = {}
#         pattern = []
#         counter = 0
#
#         for char in word:
#             if char not in char_map:
#                 char_map[char] = counter
#                 counter += 1
#             pattern.append(str(char_map[char]))
#
#         return ''.join(pattern)
#
#     # 각 단어의 패턴을 계산하여 그룹화
#     pattern_count = defaultdict(int)
#
#     for word in input_data:
#         pattern = get_pattern(word)
#         pattern_count[pattern] += 1
#
#     # 같은 패턴을 가진 단어들의 조합 개수 계산 (nC2)
#     output_data = 0
#     for count in pattern_count.values():
#         output_data += count * (count - 1) // 2
#
#     return output_data


if __name__ == "__main__":
    n, input_data = read_input()
    output_data = solve(n, input_data)
    write_output(output_data)
