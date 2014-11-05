# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ConfigParser import ConfigParser
from items import *
import MySQLdb as mdb


Config = ConfigParser()
Config.read('../scrapy.cfg')

Con = mdb.connect(
    Config.get('DB', 'host'),
    Config.get('DB', 'uname'),
    Config.get('DB', 'passw'),
    Config.get('DB', 'dname')
)
Cur = Con.cursor()


profile_field_order = [
    'uid', 'url', 'name', 'social_verify', 'location',
    'num_campaigns', 'num_contrib', 'num_referrals', 'num_comments'
]
def process_profile(profile_item):
    Cur.execute(
        'INSERT INTO igg_user_profile('+
        'uid,url,name,social_verify,location,'+
        'num_campaigns,num_contrib,num_referrals,num_comments'+
        ") VALUES (%d,'%s','%s','%s','%s',%d,%d,%d,%d)"
        % tuple([process_item[key] for key in profile_field_order])
    )


def process_campaign(campaign_item):
    uid = campaign_item['uid']
    for pid in campaign_item['campaign_ids']:
        Cur.execute(
            'INSERT INTO igg_user_campaign(uid,pid) VALUES (%d,%d)' %
            (uid, pid)
        )

    for pid in campaign_item['contrib_ids']:
        cur.execute(
            'insert into igg_user_contribution(uid,pid) VALUES (%d,%d)' %
            (uid, pid)
        )

    for pid in campaign_item['following_ids']:
        cur.execute(
            'insert into igg_user_following(uid,pid) VALUES (%d,%d)' %
            (uid, pid)
        )


def process_activity(activity_item):
    uid = activity_item['uid']
    for tup in activity_item['activities']:
        if len(tup) == 4:
            Cur.execute(
                'INSERT INTO igg_user_comment(uid,pid,tlabal,content)' +
                "VALUES (%d,%d,'%s','%s')" % (uid,tup[1],tup[2],tup[3])
            )
        else:
            Cur.execute(
                'INSERT INTO igg_user_activity_log(uid,pid,tlabal,act)' +
                "VALUES (%d,%d,'%s','%s')" % (uid,tup[1],tup[2],tup[0])
            )


class IndiegogoPipeline(object):
    _process_branch = {
        UserProfileItem: process_profile,
        UserCampaignItem: process_campaign,
        UserActivityItem: process_activity
    }

    def process_item(self, item, spider):
        IndiegogoPipeline._process_branch[item.__cls__]()
        return item
