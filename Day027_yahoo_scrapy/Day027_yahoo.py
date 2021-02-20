import scrapy
from bs4 import BeautifulSoup
from Day027.items import ScrapyDemoItem

class YahooSpider(scrapy.Spider):
    name = 'yahoo'
    allowed_domains = ['tw.news.yahoo.com']
    start_urls = ['https://tw.news.yahoo.com/technology?guccounter=1']

    # 頁面滑動模擬之後再補充
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all("li", attrs={"class", "js-stream-content Pos(r)"})
        
        item = ScrapyDemoItem()        
        for d in data:
            item['title'] = d.find("h3").text
            item['content'] = d.find("p").text 
            
            yield item

