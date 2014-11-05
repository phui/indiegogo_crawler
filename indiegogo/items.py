# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserProfileItem(scrapy.Item):
    uid = scrapy.Field() # user id
    url = scrapy.Field() # source url
    name = scrapy.Field() # username
    social_verify = scrapy.Field() # verification content of social info
    location = scrapy.Field() # location string of the user
    num_campaigns = scrapy.Field() # number of campaigns started
    num_contrib = scrapy.Field() # number of contributions made
    num_referrals = scrapy.Field() # number of referrals made
    num_comments = scrapy.Field() # number of comments made


class UserSocialverifyItem(scrapy.Item):
    uid = scrapy.Field()
    verify = scrapy.Field()


class UserCampaignItem(scrapy.Item):
    uid = scrapy.Field() # user id
    # list of urls of campaigns started shown on the site
    campaign_ids = scrapy.Field()
    # list of urls of contribution shown on the site
    contrib_ids = scrapy.Field()
    # list of urls of following projects shown on the site
    following_ids = scrapy.Field()


class UserActivityItem(scrapy.Item):
    uid = scrapy.Field() # user id
    # list of activity info show on the site
    activities = scrapy.Field()


class ProjectItem(scrapy.Item):
    pass
