# mathse-scrapy
Scrape the most recent Q and A posted in math.se of the specified tag and save as LaTeX files


- First, do `pip install scrapy` (inside virtualenv, preferably)

- Then, clone the repository
    `git clone git@github.com:g-ar/mathse-scrapy.git`

- Crawl math.se
    `scrapy crawl mathsetex`

Most recent questions will be saved as tex files in the form <Q.No>.tex, which can be compiled using pdflatex