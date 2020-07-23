#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from datetime import date

base_url = 'https://www.momoclo.net/'
news_url = base_url + '/news/'

def get_date_for_momoclo_page(dt):
    year_div = dt.find("div", {"class": "year"}).string
    date_div = dt.find("div", {"class": "date"}).string
    return year_div + "/" + date_div


def get_web_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read().decode('utf-8')

def parse(soup):
    news_dict = []
    articles = soup.find_all("div", {"class": "article"})
    for article in articles:
        article_date = get_date_for_momoclo_page(article.find("dt"))
        news = {
            "date" : article_date,
            "title" : article.find("h4").string,
            "url" : base_url + article.find("a")["href"]
        }
        news_dict.append(news)
    return news_dict

def main():
    page = get_web_page(news_url)
    soup = BeautifulSoup(page, "html.parser")
    news = parse(soup)
    output = {
        "updated": date.today().strftime("%Y/%m/%d"),
        "news": news
    }
    data = json.dumps(output, ensure_ascii=False, indent=4)
    with open('data/news.json', mode="w") as f:
        f.write(data)
    print(data)


if __name__ == '__main__':
    main()