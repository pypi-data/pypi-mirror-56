import requests
import urllib.parse
import os

from lxml import html

hani_base_url = 'http://www.hani.co.kr/'
chosun_base_url = 'http://www.chosun.com/'
br_base_url = 'http://berlinreport.com/bbs/'
kakao_search_book_base_url = 'https://dapi.kakao.com/v3/search/book?'


class BRParser():
    def __init__(self, href=None):
        self.href = href

    def extract(self):
        url = br_base_url + self.href
        page = requests.get(url, allow_redirects=True)
        tree = html.fromstring(page.content)

        title = tree.xpath("//td[@id='mw_basic']/div[@class='mw_basic_view_subject']/h1/text()")
        content = tree.xpath("//div[@id='view_content']/text()")
        register = tree.xpath("//span[@class='mw_basic_view_datetime media-date']/span/text()")

        ele = dict(
            title="".join(title),
            content="".join(content),
            register="".join(register),
            url=url
        )

        return ele


class BR():  # berlinreport
    def __init__(self, limit=10):
        self.hrefs = self.get_hrefs(limit=limit)

    def get_hrefs(self, limit=10):
        page = requests.get("%s%s" % (br_base_url, "new.php"), allow_redirects=True)
        tree = html.fromstring(page.content)
        hrefs_ele = tree.xpath("//div[@class='tbl_head01 tbl_wrap']/table/tbody/tr/td[3]/a")

        hrefs = set([href.values()[0] for href in hrefs_ele])
        return [*hrefs, ][:limit]

    def article(self, index=0):
        parser = BRParser(self.hrefs[index])
        return parser.extract()


class Frip():
    def extract(self, perPage=10):
        url = "https://api.frientrip.com/Products/v5"
        filt = dict(sectionType="nearBy",
                    geoPoint=dict(lat="37.4923615",
                                  lon="127.02928809999999"),
                    category=23,
                    perPage=perPage,
                    currentPage=1)
        resp = requests.get(url, json={'filter': filt})
        return resp.json()


class HaniParser():
    def __init__(self, href=None):
        self.href = href

    def extract(self):
        url = hani_base_url + self.href
        page = requests.get(url, allow_redirects=True)
        tree = html.fromstring(page.content)

        title = tree.xpath("//div[@id='article_view_headline']/h4/span[@class='title']/text()")
        subtitle = tree.xpath("//div[@class='article-text-font-size']/div[@class='subtitle']/text()")
        content = tree.xpath("//div[@class='article-text-font-size']/div[@class='text']/text()")
        register = tree.xpath("//p[@class='date-time']/span[1]/text()")

        ele = dict(
            title="".join(title),
            subtitle="".join(subtitle),
            content="".join(content),
            register="".join(register),
            url=url
        )

        return ele


class Hani():
    def __init__(self):
        self.hrefs = self.get_hrefs()

    def get_hrefs(self, limit=10):
        page = requests.get(hani_base_url, allow_redirects=True)
        tree = html.fromstring(page.content)
        hrefs_ele = tree.xpath("//a[contains(@href,'html') and starts-with(@href,'/')]")

        hrefs = set([href.values()[0] for href in hrefs_ele])
        return [*hrefs, ][:limit]

    def article(self, index=0):
        parser = HaniParser(self.hrefs[index])
        return parser.extract()


class ChosunParser():
    def __init__(self, href=None):
        self.href = href

    def extract(self):
        page = requests.get(self.href, allow_redirects=True)
        tree = html.fromstring(page.content)

        title = tree.xpath("//h1[@id='news_title_text_id']/text()")
        content = tree.xpath("//div[@id='news_body_id']/div[@class='par']/text()")
        register = tree.xpath("//div[@id='news_body_id']/div[@class='news_date']/text()")

        ele = dict(
            title="".join(title).strip(),
            content="".join(content).strip(),
            register="".join(register).strip(),
            url=self.href
        )
        return ele


class Chosun():
    def __init__(self):
        self.hrefs = self.get_hrefs()

    def get_hrefs(self, limit=10):
        page = requests.get(chosun_base_url, allow_redirects=True)
        tree = html.fromstring(page.content)
        hrefs_ele = tree.xpath("//dl/dt/a")

        hrefs = set([href.values()[0] for href in hrefs_ele])
        return [*hrefs, ][:limit]

    def article(self, index=0):
        parser = ChosunParser(self.hrefs[index])
        return parser.extract()


class KakaoBook():
    def __init__(self):
        pass

    def search(self, **kwargs):
        kwargs['size'] = 50
        kwargs['target'] = 'title'
        kwargs['sort'] = 'accuracy'

        kakao_key = os.getenv('KAKAO_KEY')
        res = requests.get(kakao_search_book_base_url,
                           params=urllib.parse.urlencode(kwargs),
                           headers={"Authorization": "KakaoAK %s" % kakao_key})

        return res
