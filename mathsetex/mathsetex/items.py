# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MathseItem(scrapy.Item):
    ques = scrapy.Field()
    top_ans = scrapy.Field()
    link = scrapy.Field()

