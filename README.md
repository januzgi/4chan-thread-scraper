# 4chan /biz/ thread images color scraper

[> Built on the base of 4Chan Thread Scraper <](https://github.com/cipherbeta/4chan-scraper)

>A simple but easy to use and tweak thread scraper. Uses axios for getting content and cheerio to parse the HTML.

# How It Works

1. Scrapes 4chan /biz/ catalog with `scraper.js` for newest threads and then each thread for their image urls. 

2. Analyzes each jpg using Python `colorAverage.py` by resizing images to 1x1 pixels and reading the color. Uses grequests and 10 simultaneous workers to fetch data quickly. Analyzes each jpg through HSV colors to determine whether they are green or red.

3. Knowing if jpg is green or red creates a `colors.txt` where the amount of green and red images can be found with a timestamp.
