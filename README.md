# 백준 자동화 도구

백준 온라인 저지(BOJ) 문제를 로컬에서 편리하게 풀고 관리하기 위한 자동화 도구입니다.

## 주요 기능

- 백준 문제 자동 크롤링 및 세팅
- 로컬 환경에서 예제 입출력으로 자동 테스트
- 백준에 코드 자동 제출
- 랜덤 문제 선택 (난이도/태그 필터링 가능)

## 설치

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. ChromeDriver 설치 (자동 제출 기능 사용 시)

Selenium을 사용한 자동 제출을 위해서는 ChromeDriver가 필요합니다.
- [ChromeDriver 다운로드](https://chromedriver.chromium.org/)
- 또는 `selenium-manager`가 자동으로 설치 (최신 버전)

## 사용법

### 1. 문제 세팅

특정 문제를 로컬에 세팅합니다.

```bash
cd tools
python boj_setup.py [문제번호]
```

**예시:**
```bash
python boj_setup.py 1000
```

**생성되는 파일:**
```
problems/
└── 1000_A+B/
    ├── solution.py      # 문제 정보가 주석으로 포함된 풀이 파일
    ├── input1.txt       # 예제 입력 1
    ├── output1.txt      # 예제 출력 1
    ├── input2.txt       # 예제 입력 2
    └── output2.txt      # 예제 출력 2
```

### 2. 로컬 테스트

작성한 코드를 예제 입출력으로 테스트합니다.

```bash
python boj_test.py [문제번호]
```

**예시:**
```bash
python boj_test.py 1000
```

**출력 예시:**
```
📂 문제 디렉토리: problems\1000_A+B

📝 2개의 테스트 케이스를 실행합니다...

테스트 케이스 1
--------------------------------------------------
✅ 통과

테스트 케이스 2
--------------------------------------------------
✅ 통과

==================================================
✅ 모든 테스트를 통과했습니다!
```

### 3. 백준에 제출

로컬에서 작성한 코드를 백준에 자동으로 제출합니다.

```bash
python boj_submit.py [문제번호] --username [아이디] --password [비밀번호]
```

**환경변수 사용 (권장):**
```bash
# 환경변수 설정
set BOJ_USERNAME=your_username
set BOJ_PASSWORD=your_password

# 제출
python boj_submit.py 1000
```

**Linux/Mac:**
```bash
export BOJ_USERNAME=your_username
export BOJ_PASSWORD=your_password
python boj_submit.py 1000
```

### 4. 랜덤 문제 가져오기

solved.ac API를 사용하여 랜덤 문제를 선택하고 자동으로 세팅합니다.

```bash
python boj_random.py [옵션]
```

**옵션:**
- `--tier [티어]`: 난이도 지정 (bronze, silver, gold, platinum, diamond, ruby)
- `--tag [태그]`: 알고리즘 태그 지정 (dp, greedy, graph 등)

**예시:**
```bash
# 완전 랜덤
python boj_random.py

# 골드 난이도 랜덤
python boj_random.py --tier gold

# 실버 난이도 + DP 태그
python boj_random.py --tier silver --tag dp

# 그리디 알고리즘 문제
python boj_random.py --tag greedy
```

## 워크플로우 예시

### 일반적인 사용 흐름

```bash
# 1. 문제 세팅
cd tools
python boj_setup.py 1000

# 2. solution.py 파일 편집하여 문제 풀이

# 3. 로컬에서 테스트
python boj_test.py 1000

# 4. 모든 테스트 통과 시 백준에 제출
python boj_submit.py 1000

# 5. Git으로 관리
cd ..
git add problems/1000_A+B/
git commit -m "Solve: BOJ 1000 A+B"
git push
```

### 랜덤 문제로 연습

```bash
# 실버 난이도 랜덤 문제 가져오기
python boj_random.py --tier silver

# 문제 풀이 후 테스트
python boj_test.py [문제번호]

# 제출
python boj_submit.py [문제번호]
```

## 프로젝트 구조

```
algo/
├── problems/              # 문제별 디렉토리
│   ├── 1000_A+B/
│   │   ├── solution.py
│   │   ├── input1.txt
│   │   └── output1.txt
│   └── ...
├── tools/                 # 자동화 스크립트
│   ├── boj_crawler.py     # 백준 크롤러 모듈
│   ├── boj_setup.py       # 문제 세팅
│   ├── boj_test.py        # 로컬 테스트
│   ├── boj_submit.py      # 자동 제출
│   └── boj_random.py      # 랜덤 문제
├── requirements.txt       # 의존성
└── README.md             # 문서
```

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

## 문제 해결

### ChromeDriver 오류
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```
- ChromeDriver를 다운로드하여 PATH에 추가하거나
- 최신 selenium (>= 4.6.0)을 사용하면 자동으로 관리됩니다

### 인코딩 오류
- 파일 인코딩은 UTF-8을 사용합니다
- Windows에서 한글이 깨질 경우 에디터 설정을 확인하세요

### 로그인 실패
- 백준 아이디와 비밀번호를 확인하세요
- 2단계 인증이 활성화된 경우 비활성화가 필요할 수 있습니다

## 기여

이슈와 풀 리퀘스트를 환영합니다!

## 라이선스

MIT License
