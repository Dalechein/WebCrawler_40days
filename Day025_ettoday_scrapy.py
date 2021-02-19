import scrapy
from bs4 import BeautifulSoup

class EttodaySpider(scrapy.Spider):
    name = 'ettoday'
    allowed_domains = ['www.ettoday.net']
    start_urls = ['https://www.ettoday.net/news/news-list.htm']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        headline_news = soup.find(class_="part_list_2").find_all('h3')
        
        for h in headline_news:
            news = {
                'news_info': h.find("a").text.replace("\u3000","")
            }  
            
            yield news