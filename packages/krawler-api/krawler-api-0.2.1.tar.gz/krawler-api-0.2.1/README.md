## 설치

`$ pip install krawler-api`




## 사용법

### 한겨레


```python
from water.krawler import Hani
import pprint

hani = Hani()
article = hani.article()

pprint.pprint(article)

{'content': '\r\n'
            '  북한이 지난 4월 개정한 헌법에 당 우위의 전통적 경제관리 방식인 ‘대안의 사업체계’를 삭제하고, 생산 현장의 '
            '자율성을 높이며 ‘시장 요소’를 도입한 ‘사회주의기업책임관리제’를 새로 명시한 사실이 뒤늦게 확인됐다. ‘개혁적 '
            ..
            '둔 완성된 국가 형태가 헌법에 모습을 드러낼 것”이라고 말했다.\n'
            '  이제훈 선임기자 \r',
 'register': '2019-07-11 21:52',
 'subtitle': '헌법 4월 개정…김일성의 ‘대안 사업체계’ 삭제\r\n'
             ' 시장자율성 도입한 ‘사회주의기업책임제’ 명시\r\n'
             ' “국무위원장이 국가를 대표” 국가수반 공식화도\r\n',
 'title': '북 ‘김정은식 경제개혁’ 헌법에 넣었다',
 'url': 'http://www.hani.co.kr//arti/politics/defense/901528.html?_fr=mt2'}

```

### 조선일보
```python

from water import chosun

chosun = Chosun()
article = chosun.article()

pprint.pprint(article)

{'content': '코스튬 플레이와 패러디를 선보이면서 이제는 많은 사람들이 기다리는 경기 의정부고등학교의 졸업사진 촬영이 12일 '
            ...
            '단체가 학생들의 패러디 문제를 제기한 이후 학교 측에서 수위 조절에 나서 지난해에는 시사 풍자와 관련한 콘셉트가 '
            '적었다.다음은 이날 진행된 의정부고의 졸업 사진 촬영 현장 사진이다.',
 'register': '입력 2019.07.12 14:05\r\n',
 'title': "2019년 의정부고 졸업사진 촬영 현장…'화사'부터 '자스민'까지",
 'url': 'http://news.chosun.com/site/data/html_dir/2019/07/12/2019071201452.html'}
```
