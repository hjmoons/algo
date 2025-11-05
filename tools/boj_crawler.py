"""
백준 온라인 저지 문제 크롤링 모듈
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional


class BOJCrawler:
    """백준 문제 크롤러"""

    BASE_URL = "https://www.acmicpc.net"
    PROBLEM_URL = f"{BASE_URL}/problem/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_problem(self, problem_id: int) -> Optional[Dict]:
        """
        문제 정보를 크롤링합니다.

        Args:
            problem_id: 백준 문제 번호

        Returns:
            문제 정보 딕셔너리 또는 None
        """
        try:
            url = f"{self.PROBLEM_URL}{problem_id}"
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 문제 제목
            title_elem = soup.select_one('#problem_title')
            if not title_elem:
                print(f"문제 {problem_id}를 찾을 수 없습니다.")
                return None

            title = title_elem.text.strip()

            # 영문 제목 추출 (solved.ac API 사용)
            title_en = self._get_title_en(problem_id)

            # 문제 설명
            description = soup.select_one('#problem_description')
            description_text = description.get_text('\n', strip=True) if description else ""

            # 입력 설명
            input_desc = soup.select_one('#problem_input')
            input_text = input_desc.get_text('\n', strip=True) if input_desc else ""

            # 출력 설명
            output_desc = soup.select_one('#problem_output')
            output_text = output_desc.get_text('\n', strip=True) if output_desc else ""

            # 시간 제한, 메모리 제한
            limit_info = soup.select_one('#problem-info')
            time_limit = ""
            memory_limit = ""
            if limit_info:
                info_items = limit_info.select('td')
                if len(info_items) >= 2:
                    time_limit = info_items[0].text.strip()
                    memory_limit = info_items[1].text.strip()

            # 예제 입력/출력
            examples = self._parse_examples(soup)

            return {
                'id': problem_id,
                'title': title,
                'title_en': title_en,
                'description': description_text,
                'input': input_text,
                'output': output_text,
                'time_limit': time_limit,
                'memory_limit': memory_limit,
                'examples': examples,
                'url': url
            }

        except requests.RequestException as e:
            print(f"문제를 가져오는 중 오류 발생: {e}")
            return None

    def _parse_examples(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """예제 입력/출력을 파싱합니다."""
        examples = []

        # 예제 입력
        sample_inputs = soup.select('pre[id^="sample-input-"]')
        sample_outputs = soup.select('pre[id^="sample-output-"]')

        for i, (input_elem, output_elem) in enumerate(zip(sample_inputs, sample_outputs)):
            examples.append({
                'input': input_elem.text.strip(),
                'output': output_elem.text.strip()
            })

        return examples

    def _get_title_en(self, problem_id: int) -> str:
        """
        solved.ac API를 사용하여 영문 제목을 가져옵니다.
        실패 시 문제 번호를 반환합니다.

        Args:
            problem_id: 문제 번호

        Returns:
            영문 제목 또는 문제 번호
        """
        try:
            api_url = f"https://solved.ac/api/v3/problem/show"
            params = {'problemId': problem_id}

            response = requests.get(api_url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            # titleKo에서 영문/숫자만 추출하거나, tags에서 영문 이름 생성
            title_ko = data.get('titleKo', str(problem_id))

            # 간단하게 영문/숫자/하이픈/언더스코어만 남기기
            import re
            title_en = re.sub(r'[^a-zA-Z0-9\-_]', '_', title_ko)
            title_en = re.sub(r'_+', '_', title_en).strip('_')

            # 너무 길면 자르기
            if len(title_en) > 50:
                title_en = title_en[:50]

            # 유효한 영문 제목이 없으면 번호 반환
            if not title_en or title_en == '_':
                return str(problem_id)

            return title_en

        except Exception as e:
            # API 실패 시 문제 번호 반환
            return str(problem_id)

    def get_problem_from_solvedac(self, tier: Optional[str] = None,
                                   tag: Optional[str] = None) -> Optional[int]:
        """
        solved.ac API를 사용하여 랜덤 문제 번호를 가져옵니다.
        한국어 문제만 선택합니다.

        Args:
            tier: 난이도 (예: 'gold', 'silver', 'bronze')
            tag: 알고리즘 태그 (예: 'dp', 'greedy')

        Returns:
            문제 번호 또는 None
        """
        try:
            # solved.ac API 사용
            api_url = "https://solved.ac/api/v3/search/problem"
            params = {
                'query': '',
                'sort': 'random',
                'direction': 'asc',
                'page': 1
            }

            # 난이도 필터
            if tier:
                tier_map = {
                    'bronze': 'b',
                    'silver': 's',
                    'gold': 'g',
                    'platinum': 'p',
                    'diamond': 'd',
                    'ruby': 'r'
                }
                tier_prefix = tier_map.get(tier.lower(), 's')
                params['query'] += f'tier:{tier_prefix} '

            # 태그 필터
            if tag:
                params['query'] += f'#{tag} '

            # 한국어 문제만 필터링
            params['query'] += 'lang:ko '

            response = requests.get(api_url, params=params)
            response.raise_for_status()

            data = response.json()
            if data.get('items') and len(data['items']) > 0:
                return data['items'][0]['problemId']

            return None

        except Exception as e:
            print(f"solved.ac API 호출 중 오류 발생: {e}")
            return None
