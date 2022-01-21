# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

from facebook_scraper.encoders import DateEncoder


class FacebookScraperPipeline(object):
    def open_spider(self, spider):
        self.file = open("profiles.json", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        json.dump(dict(item), self.file, cls=DateEncoder)
        self.file.write("\n")
        return item
