import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from mathsetex.items import MathseItem
import os

class MathseSpider(scrapy.Spider):
    name = "mathsetex"
    allowed_domains = ["stackexchange.com"]
    start_urls = ["https://math.stackexchange.com/questions/tagged/probability"]

    def __init__(self):
        path = "./texdir/"
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise

    def parse(self, response) :
        sel = Selector(response)
        sites = sel.xpath('//div[@class="summary"]/h3//a/@href')

        for site in sites:
            newlink = 'https://math.stackexchange.com'+site.extract()
            request = Request(newlink, callback=self.parse2)
            request.meta['link'] = newlink
            yield request

    def parse2(self, response):
        sel = Selector(response)
        item = MathseItem()
        ques = ''.join(response.xpath('//div[@class="question"]//div[@class="post-text"]//text()').extract())
        ans = ''.join(response.xpath('//div[@class="answer"]//div[@class="post-text"]//text()').extract())
        item[u'ques'] = ques.encode('utf-8')   # If not encoded in utf, and keys are not taken as unicode,
        item[u'top_ans'] = ans.encode('utf-8') # it throws UnicodeDecodeError
        item[u'link'] = response.meta['link'].encode('utf-8')
        qno = item[u'link'].split("/")[4]

        with open("./texdir/"+str(qno)+".tex", "w") as f:
            f.write(r'''\documentclass[11pt]{article}
\usepackage{graphicx}
\usepackage{longtable}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{hyperref}
\begin{document}

''')
            if ans:
                f.write("Link: %s"%item[u"link"])
                f.write(r"\\[1cm]")
                f.write("\n\n")
                f.write("Que: %s"%item[u"ques"])
                f.write(r"\\[1cm]")
                f.write("\n\n")
                f.write("Ans: %s"%item[u"top_ans"])
                f.write(r"\\[1cm]")
                f.write("\n\n")
            else:
                f.write("Link: %s"%item[u"link"])
                f.write(r"\\[1cm]")
                f.write("\n\n")
                f.write("Que: %s"%item[u"ques"])
                f.write(r"\\[1cm]")
                f.write("\n\n")
            f.write(r'\end{document}')
        yield item
