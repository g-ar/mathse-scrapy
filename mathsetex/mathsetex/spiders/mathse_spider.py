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
        item['ques'] = ques
        item['top_ans'] = ans
        item['link'] = response.meta['link']
        qno = item['link'].split("/")[4]        
        
        with open("./texdir/"+str(qno)+".tex", "w") as f:
            f.write(r'''\documentclass[11pt]{article}
\usepackage{graphicx}
\usepackage{longtable}
\usepackage[margin=1in]{geometry}
\usepackage{wrapfig}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{hyperref}
\begin{document}

''')
            f.write("L: "+item['link']+r'\\[1cm]'+"\n\n"+r'\textbf{Q:} '+item['ques']+r'\\[1cm]'+"\n\n"+r'\textbf{A:} '+item['top_ans']+r'\\')
            f.write(r'\end{document}')
        yield item