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
DOWNLOAD_DELAY = 8.0
CONCURRENT_REQUESTS_PER_IP = 3
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_MAX_DELAY = 30.0
AUTOTHROTTLE_DEBUG = True

# Disable retry middlewire
RETRY_ENABLED = False

# Enable pipeline
ITEM_PIPELINES = {
    'indiegogo.pipelines.MySQLPipeline': 300
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'indiegogo (+http://www.yourdomain.com)'
