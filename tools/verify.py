"""
백준 문제 solution.py 검증 스크립트
"""
import sys
import subprocess
from pathlib import Path


def verify_solution(problem_dir: Path) -> bool:
    """
    solution.py를 input/output 파일들로 검증합니다.

    Args:
        problem_dir: 문제 디렉토리 경로

    Returns:
        모든 테스트 통과 여부
    """
    solution_path = problem_dir / "solution.py"
    if not solution_path.exists():
        print(f"[X] solution.py가 없습니다: {problem_dir}")
        return False

    # input, output 폴더 확인
    input_dir = problem_dir / "input"
    output_dir = problem_dir / "output"

    if not input_dir.exists() or not output_dir.exists():
        print(f"[X] input 또는 output 폴더가 없습니다: {problem_dir}")
        return False

    # 예제 파일 찾기
    input_files = sorted(input_dir.glob("*.txt"), key=lambda x: int(x.stem))
    if not input_files:
        print(f"[X] 입력 파일이 없습니다: {input_dir}")
        return False

    print(f"[*] 문제 디렉토리: {problem_dir.name}")
    print(f"[*] {len(input_files)}개의 테스트 케이스를 실행합니다...\n")

    all_passed = True

    for input_file in input_files:
        # 대응하는 output 파일 찾기
        test_num = input_file.stem
        output_file = output_dir / f"{test_num}.txt"
        if not output_file.exists():
            print(f"[X] 출력 파일이 없습니다: {output_file.name}")
            all_passed = False
            continue

        # solution.py 실행
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                input_data = f.read()

            result = subprocess.run(
                [sys.executable, str(solution_path)],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=problem_dir
            )

            # 예상 출력 읽기
            with open(output_file, 'r', encoding='utf-8') as f:
                expected = f.read().strip()

            actual = result.stdout.strip()

            # 결과 비교
            print(f"테스트 케이스 {test_num}")
            print("-" * 50)

            if actual == expected:
                print("[O] 통과")
            else:
                print("[X] 실패")
                print(f"\n[입력]")
                print(input_data)
                print(f"\n[예상 출력]")
                print(expected)
                print(f"\n[실제 출력]")
                print(actual)
                all_passed = False

            if result.stderr:
                print(f"\n[에러]")
                print(result.stderr)
                all_passed = False

            print()

        except subprocess.TimeoutExpired:
            print(f"[X] 테스트 케이스 {test_num}: 시간 초과")
            all_passed = False
        except Exception as e:
            print(f"[X] 테스트 케이스 {test_num}: 오류 발생 - {e}")
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("[O] 모든 테스트를 통과했습니다!")
    else:
        print("[X] 일부 테스트가 실패했습니다.")

    return all_passed


def main():
    if len(sys.argv) < 2:
        print("사용법: python verify.py <문제번호>")
        print("예시: python verify.py 1000")
        sys.exit(1)

    problem_id = sys.argv[1]

    # 문제 디렉토리 찾기
    problems_dir = Path(__file__).parent.parent / "problems"
    problem_dirs = list(problems_dir.glob(f"{problem_id}_*"))

    if not problem_dirs:
        print(f"[X] 문제 {problem_id}를 찾을 수 없습니다.")
        sys.exit(1)

    if len(problem_dirs) > 1:
        print(f"[X] 여러 개의 문제가 발견되었습니다:")
        for d in problem_dirs:
            print(f"  - {d.name}")
        sys.exit(1)

    problem_dir = problem_dirs[0]
    success = verify_solution(problem_dir)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
