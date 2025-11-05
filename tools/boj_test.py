"""
백준 문제 로컬 테스트 스크립트
예제 입력으로 solution.py를 실행하고 출력을 비교합니다.
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple


class BOJTester:
    """백준 문제 테스터"""

    def __init__(self, problem_dir: Path):
        self.problem_dir = Path(problem_dir)
        self.solution_path = self.problem_dir / "solution.py"

    def run_tests(self) -> bool:
        """
        모든 테스트 케이스를 실행합니다.

        Returns:
            모든 테스트 통과 여부
        """
        if not self.solution_path.exists():
            print(f"[X] solution.py 파일을 찾을 수 없습니다: {self.solution_path}")
            return False

        # 테스트 케이스 찾기
        test_cases = self._find_test_cases()

        if not test_cases:
            print("[!] 테스트 케이스를 찾을 수 없습니다.")
            return False

        print(f"[*] {len(test_cases)}개의 테스트 케이스를 실행합니다...\n")

        all_passed = True
        for i, (input_file, output_file) in enumerate(test_cases, 1):
            passed = self._run_single_test(i, input_file, output_file)
            if not passed:
                all_passed = False

        print("\n" + "=" * 50)
        if all_passed:
            print("[O] 모든 테스트를 통과했습니다!")
        else:
            print("[X] 일부 테스트가 실패했습니다.")

        return all_passed

    def _find_test_cases(self) -> List[Tuple[Path, Path]]:
        """테스트 케이스 파일들을 찾습니다."""
        test_cases = []
        i = 1
        while True:
            input_file = self.problem_dir / f"input{i}.txt"
            output_file = self.problem_dir / f"output{i}.txt"

            if not input_file.exists() or not output_file.exists():
                break

            test_cases.append((input_file, output_file))
            i += 1

        return test_cases

    def _run_single_test(self, test_num: int, input_file: Path, output_file: Path) -> bool:
        """단일 테스트 케이스를 실행합니다."""
        print(f"테스트 케이스 {test_num}")
        print("-" * 50)

        # 예상 출력 읽기
        with open(output_file, 'r', encoding='utf-8') as f:
            expected_output = f.read().strip()

        # 입력 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            test_input = f.read()

        # solution.py 실행
        try:
            result = subprocess.run(
                [sys.executable, str(self.solution_path)],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8'
            )

            actual_output = result.stdout.strip()

            # 출력 비교
            if actual_output == expected_output:
                print("[O] 통과")
                return True
            else:
                print("[X] 실패")
                print(f"\n[입력]")
                print(test_input.strip())
                print(f"\n[예상 출력]")
                print(expected_output)
                print(f"\n[실제 출력]")
                print(actual_output)

                # stderr가 있으면 출력
                if result.stderr:
                    print(f"\n[에러]")
                    print(result.stderr)

                return False

        except subprocess.TimeoutExpired:
            print("[X] 시간 초과 (10초)")
            return False
        except Exception as e:
            print(f"[X] 실행 중 오류 발생: {e}")
            return False
        finally:
            print()


def find_problem_dir(problem_id: str, base_dir: str = "problems") -> Path:
    """문제 번호로 문제 디렉토리를 찾습니다."""
    base_path = Path(base_dir)

    if not base_path.exists():
        return None

    # 문제 번호로 시작하는 디렉토리 찾기
    for dir_path in base_path.iterdir():
        if dir_path.is_dir() and dir_path.name.startswith(f"{problem_id}_"):
            return dir_path

    return None


def main():
    parser = argparse.ArgumentParser(description='백준 문제를 로컬에서 테스트합니다.')
    parser.add_argument('problem_id', type=str, help='백준 문제 번호 또는 문제 디렉토리 경로')
    parser.add_argument('--dir', type=str, default='problems', help='문제가 저장된 기본 디렉토리')

    args = parser.parse_args()

    # 문제 디렉토리 찾기
    if Path(args.problem_id).exists():
        # 직접 경로가 주어진 경우
        problem_dir = Path(args.problem_id)
    else:
        # 문제 번호가 주어진 경우
        problem_dir = find_problem_dir(args.problem_id, args.dir)

    if not problem_dir or not problem_dir.exists():
        print(f"[X] 문제 디렉토리를 찾을 수 없습니다: {args.problem_id}")
        sys.exit(1)

    print(f"[*] 문제 디렉토리: {problem_dir}\n")

    # 테스트 실행
    tester = BOJTester(problem_dir)
    success = tester.run_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
