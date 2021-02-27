import scrapy


class PTTArticleItem(scrapy.Item):
    url = scrapy.Field()
    article_id = scrapy.Field()
    article_author = scrapy.Field()
    article_title = scrapy.Field()
    article_date = scrapy.Field()
    article_content = scrapy.Field()
    ip = scrapy.Field()
    message_count = scrapy.Field()
    messages = scrapy.Field()