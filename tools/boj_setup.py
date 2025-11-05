"""
백준 문제 세팅 스크립트
문제를 크롤링하여 로컬 환경에 세팅합니다.
"""
import os
import sys
import argparse
from pathlib import Path
from boj_crawler import BOJCrawler


class BOJSetup:
    """백준 문제 세팅 클래스"""

    def __init__(self, base_dir: str = "problems"):
        self.base_dir = Path(base_dir)
        self.crawler = BOJCrawler()

    def setup_problem(self, problem_id: int) -> bool:
        """
        문제를 세팅합니다.

        Args:
            problem_id: 백준 문제 번호

        Returns:
            성공 여부
        """
        print(f"문제 {problem_id}를 가져오는 중...")

        # 문제 크롤링
        problem = self.crawler.get_problem(problem_id)
        if not problem:
            print("문제를 가져오는데 실패했습니다.")
            return False

        # 문제 디렉토리 생성 (번호_영문 형식)
        problem_dir = self.base_dir / f"{problem_id}_{problem['title_en']}"
        problem_dir.mkdir(parents=True, exist_ok=True)

        print(f"문제 디렉토리 생성: {problem_dir}")

        # README.md 생성 (문제 정보)
        self._create_readme_file(problem_dir, problem)

        # solution.py 생성 (간단한 템플릿)
        self._create_solution_file(problem_dir, problem)

        # 예제 입출력 파일 생성
        self._create_example_files(problem_dir, problem['examples'])

        print(f"\n문제 세팅 완료!")
        print(f"경로: {problem_dir}")
        print(f"문제 정보: {problem_dir / 'README.md'}")
        print(f"풀이 파일: {problem_dir / 'solution.py'}")
        print(f"예제 개수: {len(problem['examples'])}")

        return True

    def _create_readme_file(self, problem_dir: Path, problem: dict):
        """README.md 파일 생성 (문제 정보)"""
        readme_path = problem_dir / "README.md"

        readme_content = f'''# {problem['id']}. {problem['title']}

**난이도**: TBD
**URL**: {problem['url']}

## 문제

{problem['description']}

## 입력

{problem['input']}

## 출력

{problem['output']}

## 제한

- **시간 제한**: {problem['time_limit']}
- **메모리 제한**: {problem['memory_limit']}

## 예제

'''

        # 예제 추가
        for i, example in enumerate(problem['examples'], 1):
            readme_content += f'''### 예제 {i}

**입력**
```
{example['input']}
```

**출력**
```
{example['output']}
```

'''

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        print(f"생성: {readme_path.name}")

    def _create_solution_file(self, problem_dir: Path, problem: dict):
        """solution.py 파일 생성 (예제 입력 분석하여 템플릿 자동 생성)"""
        solution_path = problem_dir / "solution.py"

        # 예제 입력 분석하여 입력/출력 처리 함수 생성
        read_input_func, input_handler = self._analyze_input_pattern(problem['examples'])

        solution_content = f'''"""
BOJ {problem['id']} - {problem['title']}
"""

import sys

{read_input_func}

def write_output(output_data):
    """출력 데이터를 출력"""
    print(output_data)


def solve(input_data):
    # 여기에 풀이 로직만 작성
    output_data = []

    # 풀이 로직 작성

    return output_data


if __name__ == "__main__":
{input_handler}
    output_data = solve(input_data)
    write_output(output_data)
'''

        with open(solution_path, 'w', encoding='utf-8') as f:
            f.write(solution_content)

        print(f"생성: {solution_path.name}")

    def _analyze_input_pattern(self, examples: list) -> tuple:
        """
        예제 입력을 분석하여 입력 처리 로직을 생성합니다.

        Returns:
            (read_input 함수 코드, if __name__ 블록 코드) 튜플
        """
        if not examples:
            # 한 줄 입력
            read_input_func = '''
def read_input():
    """입력을 읽어서 반환"""
    return sys.stdin.readline().rstrip()
'''
            input_handler = "    input_data = read_input()"
            return read_input_func, input_handler

        # 첫 번째 예제의 입력으로 패턴 분석
        first_input = examples[0]['input'].strip()
        lines = first_input.split('\n')

        # 한 줄 입력
        if len(lines) == 1:
            read_input_func = '''
def read_input():
    """입력을 읽어서 반환"""
    return sys.stdin.readline().rstrip()
'''
            input_handler = "    input_data = read_input()"
            return read_input_func, input_handler

        # 여러 줄 입력
        read_input_func = '''
def read_input():
    """입력을 읽어서 반환"""
    input_data = []
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        input_data.append(line.rstrip())
    return input_data
'''
        input_handler = "    input_data = read_input()"
        return read_input_func, input_handler

    def _create_example_files(self, problem_dir: Path, examples: list):
        """예제 입출력 파일 생성"""
        # input, output 폴더 생성
        input_dir = problem_dir / "input"
        output_dir = problem_dir / "output"
        input_dir.mkdir(exist_ok=True)
        output_dir.mkdir(exist_ok=True)

        for i, example in enumerate(examples, 1):
            # 입력 파일 - \r 제거
            input_path = input_dir / f"{i}.txt"
            clean_input = example['input'].replace('\r', '')
            with open(input_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(clean_input)
            print(f"생성: input/{input_path.name}")

            # 출력 파일 - \r 제거
            output_path = output_dir / f"{i}.txt"
            clean_output = example['output'].replace('\r', '')
            with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(clean_output)
            print(f"생성: output/{output_path.name}")


def main():
    parser = argparse.ArgumentParser(description='백준 문제를 로컬에 세팅합니다.')
    parser.add_argument('problem_id', type=int, help='백준 문제 번호')
    parser.add_argument('--dir', type=str, default='problems', help='문제를 저장할 디렉토리')

    args = parser.parse_args()

    setup = BOJSetup(args.dir)
    success = setup.setup_problem(args.problem_id)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
