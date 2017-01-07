# mathse-scrapy
Scrape the most recent Q and A posted in math.se of the specified tag and save as LaTeX files


- First, do `pip install scrapy` (inside virtualenv, preferably)
- Then, clone the repository
   - `git clone git@github.com:g-ar/mathse-scrapy.git`
- Crawl math.se
   - `cd mathse-scrapy/mathsetex`
   - `scrapy crawl mathsetex`

Most recent 50 questions will be saved as tex files in the form `<Q.No>.tex` inside `texdir/` directory, which can be compiled using pdflatex