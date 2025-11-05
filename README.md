# 백준 알고리즘 자동화 도구

백준 온라인 저지(BOJ) 문제를 로컬에서 편리하게 풀고 관리하기 위한 Python 자동화 도구입니다.

## 주요 기능

- 백준 문제 자동 크롤링 및 세팅
- 입력 패턴 자동 분석 및 템플릿 생성
- 로컬 환경에서 예제 입출력으로 자동 테스트
- 랜덤 문제 선택 (난이도/태그 필터링, 한국어 문제만)
- Git 기반 문제 풀이 관리

## 설치

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

**필수 패키지:**
- `beautifulsoup4`: HTML 파싱
- `requests`: HTTP 요청
- `selenium`: 자동 제출 (선택)
- `webdriver-manager`: 웹드라이버 관리 (선택)

## 사용법

### 1. 문제 세팅

특정 번호의 문제를 가져와서 로컬에 세팅합니다.

```bash
python tools/boj_setup.py 1000
```

**생성되는 파일:**
```
problems/1000_A_B/
├── README.md         # 문제 설명 (제목, 설명, 입출력 형식, 제한사항, 예제)
├── solution.py       # 풀이 템플릿 (자동 생성)
├── input/
│   ├── 1.txt        # 예제 입력 1
│   └── 2.txt        # 예제 입력 2
└── output/
    ├── 1.txt        # 예제 출력 1
    └── 2.txt        # 예제 출력 2
```

### 2. 문제 풀이

`solution.py` 파일의 `solve()` 함수에 로직을 작성합니다.

**자동 생성되는 템플릿:**

```python
"""
BOJ {문제번호} - {문제제목}
"""

import sys


def read_input():
    """입력을 읽어서 반환"""
    return sys.stdin.readline().rstrip()  # 한 줄 입력 시


def write_output(output_data):
    """출력 데이터를 출력"""
    print(output_data)


def solve(input_data):
    # 여기에 풀이 로직만 작성
    output_data = []

    # 풀이 로직 작성

    return output_data


if __name__ == "__main__":
    input_data = read_input()
    output_data = solve(input_data)
    write_output(output_data)
```

**풀이 작성 규칙:**

1. `solve(input_data)` 함수에만 로직 작성
2. `solve()` 함수는 결과를 `return`으로 반환
3. 입력은 `read_input()` 함수가 자동으로 처리
4. 출력은 `write_output()` 함수가 자동으로 처리
5. 예제 입력 패턴에 따라 `read_input()` 함수가 자동 생성됨:
   - 한 줄 입력: `return sys.stdin.readline().rstrip()`
   - 여러 줄 입력: while 루프로 모든 줄을 리스트로 반환

**예시 (1000번 A+B):**

```python
def solve(input_data):
    # 여기에 풀이 로직만 작성
    a, b = map(int, input_data.split())
    output_data = a + b
    return output_data
```

**예시 (여러 줄 입력):**

```python
def solve(input_data):
    # input_data는 리스트 형태
    output_data = []

    for line in input_data:
        # 각 줄 처리
        result = process(line)
        output_data.append(result)

    return '\n'.join(output_data)
```

### 3. 풀이 검증

작성한 풀이를 예제 입출력으로 자동 검증합니다.

```bash
python tools/verify.py 1000
```

**출력 예시:**

```
[*] 문제 디렉토리: 1000_A_B
[*] 1개의 테스트 케이스를 실행합니다...

테스트 케이스 1
--------------------------------------------------
[O] 통과

==================================================
[O] 모든 테스트를 통과했습니다!
```

### 4. 랜덤 문제 가져오기

solved.ac API를 사용하여 랜덤 문제를 선택하고 자동으로 세팅합니다.
**한국어 문제만 선택됩니다.**

```bash
python tools/boj_random.py [옵션]
```

**옵션:**
- `--tier [티어]`: 난이도 지정 (bronze, silver, gold, platinum, diamond, ruby)
- `--tag [태그]`: 알고리즘 태그 지정 (dp, greedy, graph 등)
- `--dir [경로]`: 문제를 저장할 디렉토리 (기본값: problems)

**예시:**

```bash
# 완전 랜덤 (한국어 문제만)
python tools/boj_random.py

# 골드 난이도 랜덤
python tools/boj_random.py --tier gold

# 실버 난이도 + DP 태그
python tools/boj_random.py --tier silver --tag dp

# 그리디 알고리즘 문제
python tools/boj_random.py --tag greedy
```

### 5. 백준에 제출 (선택)

로컬에서 작성한 코드를 백준에 자동으로 제출합니다.

```bash
python tools/boj_submit.py [문제번호] --id [아이디] --pw [비밀번호]
```

**환경변수 사용 (권장):**

```bash
# 환경변수 설정 (Windows)
set BOJ_USERNAME=your_username
set BOJ_PASSWORD=your_password

# 환경변수 설정 (Linux/Mac)
export BOJ_USERNAME=your_username
export BOJ_PASSWORD=your_password

# 제출
python tools/boj_submit.py 1000
```

## 워크플로우 예시

### 일반적인 사용 흐름

```bash
# 1. 문제 세팅
python tools/boj_setup.py 1000

# 2. problems/1000_A_B/solution.py 파일 편집하여 문제 풀이

# 3. 로컬에서 테스트
python tools/verify.py 1000

# 4. 모든 테스트 통과 시 백준에 제출 (선택)
python tools/boj_submit.py 1000

# 5. Git으로 관리
git add problems/1000_A_B/
git commit -m "Solve: BOJ 1000 - A+B"
git push
```

### 랜덤 문제로 연습

```bash
# 실버 난이도 랜덤 문제 가져오기
python tools/boj_random.py --tier silver

# 문제 풀이 후 테스트
python tools/verify.py [문제번호]

# 제출
python tools/boj_submit.py [문제번호]
```

## 프로젝트 구조

```
algo/
├── problems/              # 문제별 디렉토리
│   └── {번호}_{영문제목}/
│       ├── README.md      # 문제 설명
│       ├── solution.py    # 풀이 템플릿
│       ├── input/         # 예제 입력 폴더
│       │   ├── 1.txt
│       │   └── 2.txt
│       └── output/        # 예제 출력 폴더
│           ├── 1.txt
│           └── 2.txt
├── tools/                 # 자동화 스크립트
│   ├── boj_crawler.py     # 백준 크롤러 모듈
│   ├── boj_setup.py       # 문제 세팅
│   ├── verify.py          # 풀이 검증
│   ├── boj_test.py        # 로컬 테스트 (구버전)
│   ├── boj_submit.py      # 자동 제출
│   └── boj_random.py      # 랜덤 문제
├── requirements.txt       # 의존성
├── README.md             # 프로젝트 문서
└── claude.md             # 상세 개발 문서
```

## 핵심 기능 설명

### 1. 입력 패턴 자동 분석

예제 입력을 분석하여 자동으로 적절한 `read_input()` 함수를 생성합니다:

- **한 줄 입력**: `sys.stdin.readline().rstrip()` 사용
- **여러 줄 입력**: while 루프로 모든 줄을 리스트로 읽기

### 2. 한국어 문제 필터링

solved.ac API의 `lang:ko` 필터를 사용하여 한국어 문제만 선택합니다.

### 3. 입출력 함수 분리

- `read_input()`: 입력 처리
- `solve()`: 풀이 로직 (사용자가 작성)
- `write_output()`: 출력 처리

이를 통해 깔끔한 코드 구조를 유지하고, 사용자는 `solve()` 함수만 작성하면 됩니다.

### 4. 개행 문자 정규화

크롤링 시 `\r` 문자를 제거하고 `\n`으로 통일하여 Windows/Linux 환경에서 일관된 동작을 보장합니다.

## 주의사항

1. **자동 제출 기능**
   - 백준 계정 정보가 필요합니다
   - 환경변수로 관리하여 보안을 유지하세요
   - `.gitignore`에 환경변수 파일을 추가하세요

2. **크롤링**
   - 백준 서버에 부담을 주지 않도록 적절히 사용하세요
   - API 요청 제한이 있을 수 있습니다

3. **테스트**
   - 로컬 테스트는 예제 입출력만 검증합니다
   - 실제 채점 시 다른 테스트 케이스로 검증됩니다

4. **입력 형식**
   - 문제마다 입력 형식이 다를 수 있습니다
   - 필요시 `read_input()` 함수를 수정하세요

## 문제 해결

### ChromeDriver 오류 (자동 제출 시)

```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```

- ChromeDriver를 다운로드하여 PATH에 추가하거나
- 최신 selenium (>= 4.6.0)을 사용하면 자동으로 관리됩니다

### 인코딩 오류

- 파일 인코딩은 UTF-8을 사용합니다
- Windows에서 한글이 깨질 경우 에디터 설정을 확인하세요

### 한국어가 아닌 문제가 나올 때

- `boj_random.py`는 자동으로 한국어 문제만 필터링합니다
- 특정 문제 번호로 세팅 시에는 언어와 무관하게 가져옵니다

## 상세 문서

더 자세한 개발 과정 및 설계 문서는 [claude.md](claude.md)를 참고하세요.

## 기여

이슈와 풀 리퀘스트를 환영합니다!

## 라이선스

개인 학습 및 연습용 프로젝트입니다.
