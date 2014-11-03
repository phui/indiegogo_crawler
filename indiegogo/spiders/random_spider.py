import random
import scrapy


class RandomSpider(scrapy.Spider):
    name = 'random'
    allowed_domains = ['indiegogo.com']
    start_urls = []

    def start_requests(self):
        pass

    def parse(self):
        pass
