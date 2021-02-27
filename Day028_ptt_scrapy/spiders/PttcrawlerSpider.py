import scrapy
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
from Day028.items import PTTArticleItem

class PttcrawlerspiderSpider(scrapy.Spider):
    name = 'PttcrawlerSpider'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/man/fastfood/DDD7/D898/M.1519294672.A.53F.html']
    cookies = {'over18':'1'}
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookies)
    
    def parse(self, response):        
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
        
        pattern = re.compile('(?<=From:\s)(.*)')
        ip = re.search(pattern, main_content.text).group()
        
        data = PTTArticleItem()
        article_id = Path(urlparse(response.url).path).stem
        data['url'] = response.url
        data['article_id'] = article_id
        data['article_author'] = article_author
        data['article_title'] = article_title
        data['article_date'] = article_date
        data['article_content'] = article_content
        data['ip'] = ip
        data['messages'] = '######'.join(messages)
        data['message_count'] = message_count
        
        yield data
        
