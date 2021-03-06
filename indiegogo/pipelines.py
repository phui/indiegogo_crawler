# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ConfigParser import ConfigParser
from items import *
import MySQLdb as mdb


Config = ConfigParser()
with open('scrapy.cfg', 'r') as f:
    Config.readfp(f)

Con = mdb.connect(
    host=Config.get('db', 'host'),
    user=Config.get('db', 'uname'),
    passwd=Config.get('db', 'passw'),
    db=Config.get('db', 'dname'),
    port=int(Config.get('db', 'port'))
)
Cur = Con.cursor()


profile_field_order = [
    'uid', 'url', 'name', 'location',
    'num_campaigns', 'num_contrib', 'num_referrals', 'num_comments'
]
def process_profile(profile_item):
    data = tuple([profile_item[key] for key in profile_field_order])
    Cur.execute(
        'INSERT INTO igg_user_profile('+
        'uid,url,name,location,'+
        'num_campaigns,num_contrib,num_referrals,num_comments'+
        ") VALUES (%d,'%s','%s','%s',%d,%d,%d,%d)" % data 
    )


def process_verify(verify_item):
    uid = verify_item['uid']
    if len(verify_item['verify']) == 0:
        Cur.execute(
            u'INSERT INTO igg_user_verify(uid,verify) VALUES (' +
            u"%d,'not yet verified')" % uid
        )
    else:
        for verify in verify_item['verify']:
            Cur.execute(
                u'INSERT INTO igg_user_verify(uid,verify) VALUES (' +
                u"%d,'%s')" % (uid, verify)
            )


def process_campaign(campaign_item):
    uid = campaign_item['uid']
    for pid in campaign_item['campaign_ids']:
        Cur.execute(
            u'INSERT INTO igg_user_campaign(uid,pid) VALUES (%d,%d)' %
            (uid, pid)
        )

    for pid in campaign_item['contrib_ids']:
        Cur.execute(
            u'insert into igg_user_contribution(uid,pid) VALUES (%d,%d)' %
            (uid, pid)
        )

    for pid in campaign_item['following_ids']:
        Cur.execute(
            u'insert into igg_user_following(uid,pid) VALUES (%d,%d)' %
            (uid, pid)
        )


def process_activity(activity_item):
    uid = activity_item['uid']
    for tup in activity_item['activities']:
        if len(tup) == 4:
            Cur.execute(
                u'INSERT INTO igg_user_comment(uid,pid,tlabal,content)' +
                u"VALUES (%d,%d,'%s','%s')" %
                (uid,tup[1],
                 tup[2].replace("'", ""),
                 tup[3].replace("'", ""))
            )
        else:
            Cur.execute(
                u'INSERT INTO igg_user_activity_log(uid,pid,tlabal,act)' +
                u"VALUES (%d,%d,'%s','%s')" % 
                (uid,tup[1],
                 tup[2].replace("'", ""),
                 tup[0].replace("'", ""))
            )


class MySQLPipeline(object):
    _process_branch = {
        UserProfileItem: process_profile,
        UserSocialverifyItem: process_verify,
        UserCampaignItem: process_campaign,
        UserActivityItem: process_activity
    }

    def __init__(self):
        self._count = 0

    def process_item(self, item, spider):
        MySQLPipeline._process_branch[type(item)](item)
        self._count += 1
        if self._count == 1:
            Con.commit()
            self._count = 0
        return item
