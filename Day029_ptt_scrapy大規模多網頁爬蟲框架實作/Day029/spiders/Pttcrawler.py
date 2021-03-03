import scrapy
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
from ..items import PTTArticleItem

class PttcrawlerSpider(scrapy.Spider):
    name = 'Pttcrawler'
    
    def __init__(self, board='DataScience'):
        self.cookies = {'over18': '1'}
        self.host = 'https://www.ptt.cc'
        self.board = board
        self.start_urls = 'https://www.ptt.cc/bbs/{}/index.html'.format(board)
        super().__init__()

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse, cookies=self.cookies)

    def parse(self, response):
        # 取得列表中的清單主體
        soup = BeautifulSoup(response.text)
        main_list = soup.find('div', class_='bbs-screen')

        # 依序檢查文章列表中的 tag, 遇到分隔線就結束，忽略這之後的文章
        for div in main_list.findChildren('div', recursive=False):
            class_name = div.attrs['class']

            # 遇到分隔線要處理的情況
            if class_name and 'r-list-sep' in class_name:
                self.log('Reach the last article')
                break

            # 遇到目標文章
            if class_name and 'r-ent' in class_name:
                div_title = div.find('div', class_='title')
                a_title = div_title.find('a', href=True)
                # 如果文章已經被刪除則跳過
                if not a_title or not a_title.has_attr('href'):
                    continue
                article_URL = urljoin(self.host, a_title['href'])
                article_title = a_title.text
                self.log('Parse article {}'.format(article_title))
                yield scrapy.Request(url=article_URL,
                                     callback=self.parse_article,
                                     cookies=self.cookies)

    def parse_article(self, response):
        # 假設網頁回應不是 200 OK 的話, 我們視為傳送請求失敗
        if response.status != 200:
            print('Error - {} is not available to access'.format(response.url))
            return

        # 將網頁回應的 HTML 傳入 BeautifulSoup 解析器, 方便我們根據標籤 (tag) 資訊去過濾尋找
        soup = BeautifulSoup(response.text)

        # 取得文章內容主體
        main_content = soup.find("div", attrs={"id":"main-content"})
        metas = main_content.select('div.article-metaline')
        
        article_author = metas[0].select('span.article-meta-value')[0].string
        article_title = metas[1].select('span.article-meta-value')[0].string
        article_date = metas[2].select('span.article-meta-value')[0].string
        article_content = main_content.text.split(metas[-1].text)[1].split('※ 發信站:')[0][:-5]
        
        push_m = main_content.find_all("span", attrs={"class", "f3 push-content"})
        messages = [m.text[1:] for m in push_m]  
        message_count = len(messages)
        
        pattern = re.compile('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*')
        ip = re.search(pattern, main_content.text).group()
 
        
        # 整理文章資訊
        data = PTTArticleItem()
        article_id = Path(urlparse(response.url).path).stem
        data['url'] = response.url
        data['article_id'] = article_id
        data['article_author'] = article_author
        data['article_title'] = article_title
        data['article_date'] = article_date
        data['article_content'] = article_content
        data['ip'] = ip
        data['messages'] = '=====分隔線====='.join(messages)
        data['message_count'] = message_count
        
        yield data
