import scrapy
from Day026.items import ScrapyDemoItem

class Ettoday2Spider(scrapy.Spider):
    name = 'ettoday2'
    allowed_domains = ['www.ettoday.net']
    
    news1 = 'https://finance.ettoday.net/news/1922328?redirect=1'
    news2 = 'https://finance.ettoday.net/news/1901447?redirect=1'
    news3 = 'https://finance.ettoday.net/news/1909879?redirect=1'
    
    start_urls = [news1, news2, news3]

    def parse(self, response):
        item = ScrapyDemoItem()
        item['title'] = response.xpath('//title/text()').get()
        item['content'] = response.xpath('//div[@itemprop="articleBody"]//p/text()').getall()
        
        yield item
