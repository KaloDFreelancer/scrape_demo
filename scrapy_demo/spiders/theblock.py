import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_demo.items import NftscrapingItem
import datetime


article_list = ['bored ape yacht club','doodles','azuki','moonbirds']
url = 'https://www.theblock.co/search?query={}'

class TheblockSpider(scrapy.Spider):
    name = 'theblock'
    allowed_domains = ['www.theblock.co']

    # rules = [Rule(LinkExtractor(allow=r'\/post\/\d+\/.*'),callback = 'parse_item',follow = False)]
    def start_requests(self):
        for collection in article_list:
            yield scrapy.Request(url.format(collection),cb_kwargs={'collection':collection})
    
    def parse(self,response,collection):
        for link in response.xpath('//div[@class="cardContainer"]/a/@href'):
            yield response.follow(link.get(),callback = self.parse_item,cb_kwargs = {'collection':collection})

    def parse_item(self, response,collection):
        article = NftscrapingItem()
        title_selector = response.xpath('//title/text()')
        article['title'] = title_selector.get()
        article['url'] = response.url
        article['datetime_crawled'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        article['collection'] = collection
        article['datetime_posted'] = (''.join(response.xpath('//div[@class = "articleMeta"]/text()').extract()).strip())[2:]
        return article
