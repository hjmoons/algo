"""
백준 자동 제출 스크립트
selenium을 사용하여 백준에 로그인하고 코드를 제출합니다.
"""
import os
import sys
import time
import argparse
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class BOJSubmitter:
    """백준 자동 제출 클래스"""

    BASE_URL = "https://www.acmicpc.net"
    LOGIN_URL = f"{BASE_URL}/login"

    def __init__(self, username: str, password: str, headless: bool = False):
        self.username = username
        self.password = password
        self.driver = None
        self.headless = headless

    def __enter__(self):
        self._init_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def _init_driver(self):
        """Chrome WebDriver 초기화"""
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def login(self) -> bool:
        """백준에 로그인합니다."""
        try:
            print("로그인 중...")
            self.driver.get(self.LOGIN_URL)

            # 로그인 폼 찾기
            username_input = self.driver.find_element(By.NAME, "login_user_id")
            password_input = self.driver.find_element(By.NAME, "login_password")

            # 로그인 정보 입력
            username_input.send_keys(self.username)
            password_input.send_keys(self.password)

            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.ID, "submit_button")
            login_button.click()

            # 로그인 성공 확인
            time.sleep(2)

            # 로그인 실패 시 에러 메시지가 표시됨
            try:
                error = self.driver.find_element(By.CLASS_NAME, "alert-danger")
                print(f"❌ 로그인 실패: {error.text}")
                return False
            except:
                print("✅ 로그인 성공")
                return True

        except Exception as e:
            print(f"❌ 로그인 중 오류 발생: {e}")
            return False

    def submit(self, problem_id: int, code_path: Path, language: str = "Python 3") -> bool:
        """
        코드를 제출합니다.

        Args:
            problem_id: 문제 번호
            code_path: 코드 파일 경로
            language: 언어 (기본값: Python 3)

        Returns:
            제출 성공 여부
        """
        try:
            # 코드 읽기
            with open(code_path, 'r', encoding='utf-8') as f:
                code = f.read()

            print(f"문제 {problem_id}에 코드를 제출합니다...")

            # 제출 페이지로 이동
            submit_url = f"{self.BASE_URL}/submit/{problem_id}"
            self.driver.get(submit_url)

            # 언어 선택
            language_select = self.driver.find_element(By.NAME, "language")
            for option in language_select.find_elements(By.TAG_NAME, "option"):
                if language in option.text:
                    option.click()
                    break

            # 코드 입력
            code_editor = self.driver.find_element(By.ID, "source")
            self.driver.execute_script("arguments[0].value = arguments[1];", code_editor, code)

            # 제출 버튼 클릭
            submit_button = self.driver.find_element(By.ID, "submit_button")
            submit_button.click()

            print("✅ 제출 완료")

            # 결과 페이지 대기
            time.sleep(2)

            # 결과 확인 (선택사항)
            self._check_result()

            return True

        except Exception as e:
            print(f"❌ 제출 중 오류 발생: {e}")
            return False

    def _check_result(self):
        """제출 결과를 확인합니다."""
        try:
            # 상태 페이지로 이동
            status_url = f"{self.BASE_URL}/status?user_id={self.username}"
            self.driver.get(status_url)

            print("\n제출 결과를 확인하는 중...")
            print("(채점 중일 수 있습니다. 백준 사이트에서 직접 확인하세요)")

            # 최신 제출 결과 확인
            time.sleep(3)
            result_row = self.driver.find_element(By.CSS_SELECTOR, "#status-table tbody tr")
            result = result_row.find_element(By.CSS_SELECTOR, "td.result")

            print(f"\n📊 최신 제출 결과: {result.text}")

        except Exception as e:
            print(f"⚠️  결과 확인 중 오류: {e}")


def find_problem_dir(problem_id: str, base_dir: str = "problems") -> Optional[Path]:
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
    parser = argparse.ArgumentParser(description='백준에 코드를 자동으로 제출합니다.')
    parser.add_argument('problem_id', type=str, help='백준 문제 번호')
    parser.add_argument('--username', type=str, help='백준 아이디 (환경변수 BOJ_USERNAME 사용 가능)')
    parser.add_argument('--password', type=str, help='백준 비밀번호 (환경변수 BOJ_PASSWORD 사용 가능)')
    parser.add_argument('--dir', type=str, default='problems', help='문제가 저장된 디렉토리')
    parser.add_argument('--headless', action='store_true', help='헤드리스 모드로 실행')

    args = parser.parse_args()

    # 로그인 정보 가져오기
    username = args.username or os.getenv('BOJ_USERNAME')
    password = args.password or os.getenv('BOJ_PASSWORD')

    if not username or not password:
        print("❌ 백준 아이디와 비밀번호를 제공해야 합니다.")
        print("방법 1: --username과 --password 옵션 사용")
        print("방법 2: BOJ_USERNAME과 BOJ_PASSWORD 환경변수 설정")
        sys.exit(1)

    # 문제 디렉토리 찾기
    problem_dir = find_problem_dir(args.problem_id, args.dir)

    if not problem_dir:
        print(f"❌ 문제 디렉토리를 찾을 수 없습니다: {args.problem_id}")
        sys.exit(1)

    solution_path = problem_dir / "solution.py"

    if not solution_path.exists():
        print(f"❌ solution.py 파일을 찾을 수 없습니다: {solution_path}")
        sys.exit(1)

    print(f"📂 문제 디렉토리: {problem_dir}")
    print(f"📄 코드 파일: {solution_path}\n")

    # 제출
    with BOJSubmitter(username, password, args.headless) as submitter:
        if not submitter.login():
            sys.exit(1)

        success = submitter.submit(int(args.problem_id), solution_path)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
