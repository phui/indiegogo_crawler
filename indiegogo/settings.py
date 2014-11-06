# -*- coding: utf-8 -*-

# Scrapy settings for indiegogo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'GPCrawler'

SPIDER_MODULES = ['indiegogo.spiders']
NEWSPIDER_MODULE = 'indiegogo.spiders'

# Setting for delay of requests
CONCURRENT_REQUESTS_PER_IP = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_ITEMS = 1

# Disable retry middlewire
RETRY_ENABLED = False

# Enable pipeline
ITEM_PIPELINES = {
    'indiegogo.pipelines.MySQLPipeline': 300
}

# Enable random rotate of user agent strings
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'indiegogo.middlewares.RotateUserAgentMiddleware' :375,
        'indiegogo.middlewares.DelayRequestMiddleware' :200
}
