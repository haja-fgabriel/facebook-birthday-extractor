# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os

from facebook_scraper.encoders import DateEncoder

PROFILES_OUTPUT_FILE = os.getenv("PROFILES_OUTPUT_FILE", "profiles.json")


class FacebookScraperPipeline(object):
    def open_spider(self, spider):
        self.file = open(PROFILES_OUTPUT_FILE, "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        json.dump(dict(item), self.file, cls=DateEncoder)
        self.file.write("\n")
        return item
