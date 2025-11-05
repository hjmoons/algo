# BOJ 문제 풀이 자동화 프로젝트

## 프로젝트 개요

백준 알고리즘 문제를 자동으로 크롤링하고, 로컬 환경에 세팅하여 풀이할 수 있도록 돕는 Python 기반 자동화 도구입니다.

## 주요 기능

1. **문제 크롤링**: 백준 웹사이트에서 문제 정보 자동 수집
2. **로컬 세팅**: 문제 디렉토리 및 파일 자동 생성
3. **테스트 검증**: 예제 입출력으로 풀이 자동 검증
4. **Git 관리**: 풀이한 문제를 버전 관리

## 프로젝트 구조

```
algo/
├── problems/              # 문제 디렉토리
│   └── {번호}_{영문제목}/
│       ├── README.md      # 문제 설명
│       ├── solution.py    # 풀이 파일
│       ├── input/         # 입력 예제 폴더
│       │   ├── 1.txt
│       │   ├── 2.txt
│       │   └── ...
│       └── output/        # 출력 예제 폴더
│           ├── 1.txt
│           ├── 2.txt
│           └── ...
├── tools/                 # 도구 스크립트
│   ├── boj_crawler.py     # 문제 크롤러
│   ├── boj_setup.py       # 문제 세팅
│   ├── verify.py          # 풀이 검증
│   ├── boj_test.py        # 로컬 테스트
│   ├── boj_submit.py      # 자동 제출
│   └── boj_random.py      # 랜덤 문제 선택
├── requirements.txt       # 의존성
└── README.md             # 프로젝트 설명
```

## 설치 및 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 필요한 패키지

- `beautifulsoup4`: HTML 파싱
- `requests`: HTTP 요청
- `selenium`: 자동 제출 (선택)
- `webdriver-manager`: 웹드라이버 관리 (선택)

## 사용 방법

### 1. 문제 세팅

특정 번호의 문제를 가져와서 로컬에 세팅합니다.

```bash
python tools/boj_setup.py 1000
```

**생성되는 파일:**
- `problems/1000_A_B/README.md`: 문제 설명 (제목, 설명, 입출력 형식, 제한사항, 예제)
- `problems/1000_A_B/solution.py`: 풀이 템플릿
- `problems/1000_A_B/input/1.txt, 2.txt, ...`: 입력 예제
- `problems/1000_A_B/output/1.txt, 2.txt, ...`: 출력 예제

### 2. 문제 풀이

`solution.py` 파일의 `solve()` 함수에 로직을 작성합니다.

**템플릿 구조:**

```python
"""
BOJ {문제번호} - {문제제목}
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

### 4. 랜덤 문제 선택 (선택)

특정 난이도의 랜덤 문제를 선택합니다.

```bash
python tools/boj_random.py --tier gold
```

### 5. 자동 제출 (선택)

Selenium을 사용하여 백준에 자동으로 제출합니다.

```bash
python tools/boj_submit.py 1000 --id {백준ID} --pw {비밀번호}
```

## 핵심 설계 원칙

### 1. 입력 처리 방식

- **표준 입력 사용**: `sys.stdin.readline()` 사용
- **파라미터 전달**: `if __name__ == "__main__":`에서 입력을 읽어 `solve()` 함수에 전달
- **유연한 구조**: 문제마다 입력 형식이 다르므로, 입력 처리 로직은 필요에 따라 수정 가능

### 2. 파일 구조

- **입출력 분리**: `input/`, `output/` 폴더로 예제 파일 분리
- **숫자 기반 네이밍**: `1.txt`, `2.txt` 형식으로 순서 관리
- **영문 디렉토리명**: `{번호}_{영문제목}` 형식 (solved.ac API 활용)

### 3. 개행 문자 처리

- 크롤링 시 `\r` 제거: Windows 스타일 개행 문자 제거
- `newline='\n'` 사용: 일관된 Unix 스타일 개행 문자 사용

## 주요 스크립트 설명

### boj_crawler.py

- 백준 웹사이트에서 HTML 크롤링
- solved.ac API로 영문 제목 가져오기
- 문제 설명, 입출력 형식, 예제 수집

### boj_setup.py

- 문제 디렉토리 생성
- README.md 파일 생성 (문제 정보)
- solution.py 템플릿 생성
- input/output 폴더 및 예제 파일 생성

### verify.py

- solution.py 실행
- 예제 입력으로 테스트
- 실제 출력과 예상 출력 비교
- 통과/실패 결과 출력

### boj_test.py (구버전, verify.py 권장)

- 로컬 테스트 실행
- subprocess로 solution.py 실행

### boj_submit.py (선택)

- Selenium으로 백준 로그인
- 소스 코드 자동 제출

### boj_random.py (선택)

- solved.ac API로 랜덤 문제 선택
- 난이도, 태그 필터링

## 예제 워크플로우

1. **문제 선택 및 세팅**
   ```bash
   python tools/boj_setup.py 1000
   ```

2. **문제 읽기**
   - `problems/1000_A_B/README.md` 확인

3. **풀이 작성**
   - `problems/1000_A_B/solution.py` 편집
   - `solve()` 함수에 로직 작성

4. **로컬 검증**
   ```bash
   python tools/verify.py 1000
   ```

5. **제출** (선택)
   ```bash
   python tools/boj_submit.py 1000
   ```

6. **Git 커밋**
   ```bash
   git add problems/1000_A_B/
   git commit -m "Solve: BOJ 1000 - A+B"
   ```

## 향후 개선 사항

- [ ] 입력 형식 자동 분석 및 템플릿 생성
- [ ] 문제 난이도 자동 추가 (solved.ac API)
- [ ] 다국어 지원 (영문 문제)
- [ ] 통계 및 진행도 추적
- [ ] 웹 UI 추가

## 주의 사항

1. **크롤링 주의**: 백준 서버에 부하를 주지 않도록 적절한 간격으로 요청
2. **자동 제출 주의**: 백준 이용 약관 확인 필요
3. **입력 형식**: 문제마다 입력 형식이 다르므로 템플릿 수정 필요
4. **개행 문자**: Windows 환경에서 `\r\n` 처리 주의

## 라이선스

개인 학습 및 연습용 프로젝트입니다.
