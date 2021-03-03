import scrapy
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
from Day029.items import PTTArticleItem

class PttcrawlerSpider(scrapy.Spider):
    name = 'Pttcrawler'
    
    def __init__(self, board='DataScience'):
        self.cookies = {'over18':'1'}
        self.host = 'https://www.ptt.cc'
        self.board = board
        self.start_urls = 'https://www.ptt.cc/bbs/{}/index.html'.format(board)
        super().__init__()   
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=self.start_urls, callback=self.parse, cookies=self.cookies)
    
    def parse(self, response): 
        soup = BeautifulSoup(response.text, 'lxml')
        main_list = soup.find_all("div", attrs={"class":"r-list-container action-bar-margin bbs-screen"})
        for div in main_list:
            div_title = div.find("div", attrs={"class","title"})
            article_link = div_title.a['href']
            article_URL = urljoin(self.host, article_link)
            article_title = div_title.a.string        
            yield scrapy.Request(url=article_URL, callback=self.parse_article, cookies=self.cookies)   
            
    def parse_article(self, response):        
        # 假設網頁回應不是 200 OK 的話, 我們視為傳送請求失敗
        if response.status != 200:
            print('Error - {} is not available to access'.format(response.url))
            return
        
        soup = BeautifulSoup(response.text, 'lxml')        
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
        try:
            ip = re.search(pattern, main_content.text).group()
        except Exception as e:
            ip = ''
        
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
        
        #return data
        
        yield data