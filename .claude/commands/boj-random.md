---
description: 랜덤 백준 문제를 가져옵니다
args:
  tier:
    description: 난이도 (bronze/silver/gold/platinum/diamond/ruby)
    required: false
  tag:
    description: 알고리즘 태그 (dp/greedy/graph 등)
    required: false
---

python tools/boj_random.py{{#if tier}} --tier {{tier}}{{/if}}{{#if tag}} --tag {{tag}}{{/if}}

**중요: 모든 응답은 반드시 한글로 작성해야 합니다.**
