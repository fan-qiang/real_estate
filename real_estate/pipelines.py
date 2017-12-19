# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from pymysql.cursors import DictCursor
from twisted.enterprise import adbapi

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class RealEstatePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        db_args = {
            'host': self.settings.get('MYSQL_HOST', 'localhost'),
            'port': self.settings.get('MYSQL_PORT', 3306),
            'user': self.settings.get('MYSQL_USER', None),
            'password': self.settings.get('MYSQL_PASSWORD', ''),
            'db': self.settings.get('MYSQL_DB', None),
            'charset': 'utf8',
            'cursorclass': DictCursor,
            'cp_reconnect': True,
        }
        self.retries = self.settings.get('MYSQL_RETRIES', 3)
        self.close_on_error = self.settings.get('MYSQL_CLOSE_ON_ERROR', True)
        self.db = adbapi.ConnectionPool('pymysql', **db_args)

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        query = self.db.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread

        columns = lambda d: ', '.join(['`{}`'.format(k) for k in d])
        values = lambda d: [v for v in d.values()]
        placeholders = lambda d: ', '.join(['%s'] * len(d))

        on_duplicate_placeholders = lambda d: ', '.join(['`{}` = %s'.format(k) for k in d])

        sql_template = "insert into `real_estate`  ( {} ) VALUES ( {} ) ON DUPLICATE KEY UPDATE {}"

        tx.execute(sql_template.format(columns(item), placeholders(item),on_duplicate_placeholders(item)),
                   values(item) + values(item))

        logger.info("Item stored in db: %s" % item)

    def handle_error(self, e):
        logger.error(e)




