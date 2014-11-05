import random
import scrapy
from scrapy.http import Request
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
        profile['uid'] = int(response.url.split('/')[-1])
        profile['url'] = response.url

        profile['name'] = response.css(
            'body > div.container.i-profile-header > div.row > ' +
            'div.col-sm-8.i-margin-bottom-20 > h1::text'
        ).extract()[0]

        social_verify = response.css(
            'body > div.container.i-profile-container > div > div ' +
            '> div.col-sm-4 > div:nth-child(3) > ' +
            'div.i-framed.i-verifications > div > ' +
            'span:nth-child(2)::text'
        ).extract()[0]
        if len(social_verify.split()) > 2:
            social_verify = -1
        else:
            social_verify = int(''.join(social_verify.split()[0].split(',')))
        profile['social_verify'] = social_verify

        profile['location'] = response.css(
            'body > div.container.i-profile-header > div.row > ' +
            'div.col-sm-8.i-margin-bottom-20 > div > span:nth-child(2)::text'
        ).extract()[0]

        stats = response.css(
            'body > div.container.i-profile-container > div > div > ' +
            'div.col-sm-4 > ul > li > em::text'
        ).extract()
        stats = [int(''.join(ele.split(','))) for ele in stats]
        profile['num_campaigns'], profile['num_comments'],\
                profile['num_contrib'], profile['num_referrals'] = stats

        # yield the parsed result from the campaigns page
        yield Request(self.url + '/campaigns', callback=self.parse_campaign)
        # yield the parsed result from the activity page
        yield Request(self.url + '/activities', callback=self.parse_activity)
        return profile

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
        return campaigns

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
                acts.append((act_types[i], act_project_ids[i], act_time_labels[i])
        activity['activities'] = acts

        return activity
