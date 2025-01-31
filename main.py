#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from datetime import date

base_url = "https://www.momoclo.net"
news_url = base_url + "/news/"


def get_web_page(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req).read().decode("utf-8")


def parse(soup):
    news_dict = []
    articles = soup.find_all("div", {"class": "news_list_container"})
    for article in articles:
        article_date = article.find("p", {"class": "news_list_date"}).string.replace(
            ".", "/"
        )
        article_title = article.find("p", {"class": "news_list_text"}).string
        article_url = article.find("a", {"class": "news_list_link"})["href"]
        news = {
            "date": article_date,
            "title": article_title,
            "url": article_url,
        }
        news_dict.append(news)
    return news_dict


def main():
    page = get_web_page(news_url)
    soup = BeautifulSoup(page, "html.parser")
    news = parse(soup)
    output = {"updated": date.today().strftime("%Y/%m/%d"), "news": news}
    with open("data/news.json", mode="w") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
