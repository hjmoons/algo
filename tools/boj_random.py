"""
백준 랜덤 문제 가져오기 스크립트
solved.ac API를 사용하여 랜덤 문제를 가져와서 자동으로 세팅합니다.
"""
import sys
import argparse
import random
from boj_crawler import BOJCrawler
from boj_setup import BOJSetup


class BOJRandom:
    """백준 랜덤 문제 선택 클래스"""

    TIER_LEVELS = {
        'bronze': list(range(1, 6)),      # Bronze V ~ I
        'silver': list(range(6, 11)),     # Silver V ~ I
        'gold': list(range(11, 16)),      # Gold V ~ I
        'platinum': list(range(16, 21)),  # Platinum V ~ I
        'diamond': list(range(21, 26)),   # Diamond V ~ I
        'ruby': list(range(26, 31)),      # Ruby V ~ I
    }

    def __init__(self):
        self.crawler = BOJCrawler()

    def get_random_problem(self, tier: str = None, tag: str = None) -> int:
        """
        랜덤 문제를 가져옵니다.

        Args:
            tier: 난이도 티어 (bronze, silver, gold, platinum, diamond, ruby)
            tag: 알고리즘 태그 (예: dp, greedy, graph 등)

        Returns:
            문제 번호
        """
        # solved.ac API 사용
        problem_id = self.crawler.get_problem_from_solvedac(tier=tier, tag=tag)

        if problem_id:
            return problem_id

        # API 실패 시 대체 방법: 간단한 랜덤 생성
        print("⚠️  solved.ac API 사용 실패, 랜덤 문제 번호 생성...")
        return random.randint(1000, 20000)

    def setup_random_problem(self, tier: str = None, tag: str = None,
                            base_dir: str = "problems") -> bool:
        """
        랜덤 문제를 가져와서 세팅합니다.

        Args:
            tier: 난이도 티어
            tag: 알고리즘 태그
            base_dir: 문제를 저장할 디렉토리

        Returns:
            성공 여부
        """
        print("[*] 랜덤 문제를 선택하는 중...")

        if tier:
            print(f"   난이도: {tier.upper()}")
        if tag:
            print(f"   태그: {tag}")

        # 랜덤 문제 번호 가져오기
        problem_id = self.get_random_problem(tier=tier, tag=tag)

        if not problem_id:
            print("[X] 랜덤 문제를 가져오는데 실패했습니다.")
            return False

        print(f"\n[+] 선택된 문제: {problem_id}번\n")

        # 문제 세팅
        setup = BOJSetup(base_dir)
        return setup.setup_problem(problem_id)


def main():
    parser = argparse.ArgumentParser(
        description='백준 랜덤 문제를 가져와서 세팅합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python boj_random.py                    # 완전 랜덤
  python boj_random.py --tier gold        # 골드 난이도 랜덤
  python boj_random.py --tier silver --tag dp    # 실버 + DP 태그
  python boj_random.py --tag greedy       # 그리디 태그 랜덤

티어 목록:
  bronze, silver, gold, platinum, diamond, ruby

주요 태그 예시:
  dp, greedy, graph, implementation, bruteforcing,
  bfs, dfs, math, sort, string, etc.
        """
    )

    parser.add_argument(
        '--tier',
        type=str,
        choices=['bronze', 'silver', 'gold', 'platinum', 'diamond', 'ruby'],
        help='난이도 티어 선택'
    )

    parser.add_argument(
        '--tag',
        type=str,
        help='알고리즘 태그 (예: dp, greedy, graph)'
    )

    parser.add_argument(
        '--dir',
        type=str,
        default='problems',
        help='문제를 저장할 디렉토리 (기본값: problems)'
    )

    args = parser.parse_args()

    # 랜덤 문제 세팅
    random_picker = BOJRandom()
    success = random_picker.setup_random_problem(
        tier=args.tier,
        tag=args.tag,
        base_dir=args.dir
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
