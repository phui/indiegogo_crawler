import random
import scrapy
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from ConfigParser import ConfigParser


Config = ConfigParser()
Config.read('../../scrapy.cfg')

uid_high = Config.get('uid', 'high')
uid_low = Config.get('uid', 'low')
url_format = Config.get('url', 'format')

class RandomSpider(scrapy.Spider):
    name = 'random'
    allowed_domains = ['indiegogo.com']
    start_urls = []

    def start_requests(self):
        while True:
            yield Request(url_format % random.randint(uid_low, uid_high), self.parse)

    def parse(self, response):
        profile = UserProfileItem()
        response.css('some path').extract()

        # yield the parsed result from the campaigns page
        yield Request(self.url + '/campaigns', callback=self.parse_campaign)
        # yield the parsed result from the activity page
        yield Request(self.url + '/activities', callback=self.parse_activity)
        return profile

    def parse_campaign(self, response):
        pass

    def parse_activity(self, response):
        pass
