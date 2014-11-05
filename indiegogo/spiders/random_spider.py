import random
import scrapy
from scrapy.http import Request
from ConfigParser import ConfigParser
from indiegogo.items import *


Config = ConfigParser()
with open('scrapy.cfg', 'r') as f:
    Config.readfp(f)

uid_high = Config.get('uid', 'high')
uid_low = Config.get('uid', 'low')
url_format = Config.get('url', 'format')

class RandomSpider(scrapy.Spider):
    name = 'random'
    allowed_domains = ['indiegogo.com']
    start_urls = [
        'https://indiegogo.com/individuals/91221',
        'https://www.indiegogo.com/individuals/9023673'
    ]

    #def start_requests(self):
    #    while True:
    #        yield Request(url_format % random.randint(uid_low, uid_high), self.parse)

    def parse(self, response):
        profile = UserProfileItem()
        uid = int(response.url.split('/')[-1])
        profile['uid'] = uid
        profile['url'] = response.url

        profile['name'] = response.css(
            'body > div.container.i-profile-header > div.row > ' +
            'div.col-sm-8.i-margin-bottom-20 > h1::text'
        ).extract()[0]

        verifications = response.css(
            'body > div.container.i-profile-container > div > div > ' +
            'div.col-sm-4 > div.i-lined-section > ' +
            'div.i-framed.i-verifications > div > span::text'
        ).extract()
        social_verify = UserSocialverifyItem()
        social_verify['uid'] = uid
        social_verify['verify'] = verifications
        yield social_verify

        location = response.css(
            'body > div.container.i-profile-header > div.row > ' +
            'div.col-sm-8.i-margin-bottom-20 > div > span:nth-child(2)::text'
        ).extract()
        profile['location'] = location[0] if len(location) > 0 else 'not shown'

        stats = response.css(
            'body > div.container.i-profile-container > div > div > ' +
            'div.col-sm-4 > ul > li > em::text'
        ).extract()
        stats = [int(''.join(ele.split(','))) for ele in stats]
        profile['num_campaigns'], profile['num_comments'],\
                profile['num_contrib'], profile['num_referrals'] = stats

        # yield the parsed result from the campaigns page
        yield Request(response.url + '/campaigns', callback=self.parse_campaign)
        # yield the parsed result from the activity page
        yield Request(response.url + '/activities', callback=self.parse_activity)
        yield profile

    def parse_campaign(self, response):
        campaign = UserCampaignItem()
        campaign['uid'] = int(response.url.split('/')[-2])

        campaign['campaign_ids'] = [
            int(e.split('/')[-1]) for e in response.css(
                'body > div.container.i-profile-container > div:nth-child(1) > ' +
                'ul > li > div > div.i-campaign > a::attr(href)'
            ).extract()
        ]

        campaign['contrib_ids'] = [
            int(e.split('/')[-1]) for e in response.css(
                'body > div.container.i-profile-container > div:nth-child(2) > ' +
                'ul > li > div > div.i-campaign > a::attr(href)'
            ).extract()
        ]

        campaign['following_ids'] = [
            int(e.split('/')[-1]) for e in response.css(
                'body > div.container.i-profile-container > div:nth-child(3) > ' +
                'ul > li > div > div.i-campaign > a::attr(href)'
            ).extract()
        ]
        return campaign

    def parse_activity(self, response):
        activity = UserActivityItem()
        activity['uid'] = int(response.url.split('/')[-2])

        act_types = [
            e.strip(' ,\n:').split()[0].lower()
            for e in response.css(
                'body > div.container.i-profile-container > div > ul > li >' +
                ' div > div.i-activity-prefix::text'
            ).extract()
        ]

        act_project_ids = [
            int(e.split('/')[-1]) for e in response.css(
                'body > div.container.i-profile-container > div > ul > li >' +
                ' div > div.i-campaign > a::attr(href)'
            ).extract()
        ]

        act_time_labels = [
            ' '.join(e.split()[0:-1]).lower() for e in response.css(
                'body > div.container.i-profile-container > div > ul > li >' +
                ' div > div.i-time-ago::text'
            ).extract()
        ]

        comments_content = response.css(
            'body > div.container.i-profile-container > div >' +
            ' ul > li > div > p::text'
        ).extract()

        num_act = len(act_types)
        comment_counter = 0
        acts = list()
        for i in range(num_act):
            if act_types[i] == 'commented':
                acts.append(
                    (act_types[i], act_project_ids[i],
                     act_time_labels[i], comments_content[comment_counter])
                )
                comment_counter += 1
            else:
                acts.append((act_types[i], act_project_ids[i], act_time_labels[i]))
        activity['activities'] = acts

        return activity
