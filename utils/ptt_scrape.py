import re
import time
import urllib.parse
import datetime
import logging
import json
from requests_html import HTMLSession
import os
import sys
import pandas as pd
from utils.app_manager import AppManager

# 設定常數與靜態資料
BASE_URL = "https://www.ptt.cc"
EXCLUDE_KEYWORDS = {
    "公告",
    "炸裂",
    "發錢",
    "轉播",
    "Live",
    "live",
    "BOX",
    "Re",
    "英超",
    "Schedule",
    "Standings",
    "SSD選購指南碎念之邁向八週年",
    "選購指南",
    "音效卡保固挖坑",
    "大雪注意報",
    "置底",
    "指定通路",
    "用卡整理",
    "賽程",
    "專區",
    "發佈",
    "作品首播",
    "賽籤表",
    "售票資訊",
    "集中",
    "捐血贈品",
}


class PttScraper:
    BASE_URL = "https://www.ptt.cc"

    def __init__(self, board, push_thresh=50, par_day="today"):
        self.board = board
        self.push_thresh = push_thresh
        self.session = HTMLSession()
        self.session.cookies.set("over18", "1")
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        self.par_day = self.get_par_day(par_day)
        self.app_manger = AppManager()

    def get_par_day(self, par_day):
        """取得日期，若為今日則為今天的日期，否則為昨日日期"""
        today = datetime.datetime.now()
        return (
            today.strftime("%m/%d").lstrip("0")
            if par_day == "today"
            else (today - datetime.timedelta(days=1)).strftime("%m/%d").lstrip("0")
        )

    def fetch_page(self, url):
        try:
            return self.session.get(url)
        except Exception as e:
            logging.error(f"無法獲取頁面: {url}, 錯誤: {e}")
            return None

    def parse_articles(self, elements):
        """從網頁提取文章資訊"""
        articles = []
        for element in elements:
            try:
                article = self.extract_article_data(element)
                if article:
                    articles.append(article)
            except AttributeError:
                continue
        return articles

    def extract_article_data(self, element):
        """抽取單篇文章的資料"""
        push = element.find(".nrec", first=True).text or "0"
        title = element.find(".title", first=True).text or ""
        author = element.find(".meta > .author", first=True).text or ""
        date = element.find(".meta > .date", first=True).text or ""
        link = self.BASE_URL + element.find(".title > a", first=True).attrs.get(
            "href", ""
        )

        # 若標題中有刪除的訊息，提取作者名
        if "(本文已被刪除)" in title:
            match_author = re.search(r"\[(\w+)\]", title)
            author = match_author.group(1) if match_author else author

        return {
            "push": push,
            "title": title,
            "author": author,
            "date": date,
            "link": link,
        }

    def get_next_page(self, controls):
        return urllib.parse.urljoin(self.BASE_URL, controls[1].attrs["href"])

    def filter_articles(self, articles, pre_title):
        """過濾符合條件的文章並更新最早日期"""
        filtered_articles = []
        earliest_date = None
        for article in articles:
            title = article["title"].translate(str.maketrans("", "", "[]"))

            if pre_title == title:
                return filtered_articles, earliest_date, True  # 停止條件

            if not self.rm_keywords(title):
                continue

            earliest_date = (
                min(earliest_date, article["date"])
                if earliest_date
                else article["date"]
            )

            if self.is_article_valid(title, article):
                filtered_articles.append(article)

        return filtered_articles, earliest_date, False

    def rm_keywords(self, title):
        """排除包含關鍵字的文章"""
        if any(keyword in title for keyword in EXCLUDE_KEYWORDS):
            return False
        else:
            return True

    def is_article_valid(self, title, article):
        """檢查文章是否符合推文數量與排除條件"""
        if "X" in article["push"]:
            return False
        if article["date"] == self.par_day and (
            article["push"] == "爆"
            or (article["push"].isdigit() and int(article["push"]) >= self.push_thresh)
        ):
            return True
        return False

    def scrape(self):
        """開始抓取並處理資料"""
        url = f"{BASE_URL}/bbs/{self.board}/index.html"
        result = []
        pre_title = self.app_manger.read_last_line(self.board)

        start_time = time.time()
        while True:
            response = self.fetch_page(url)
            if not response:
                break

            articles = self.parse_articles(response.html.find("div.r-ent"))
            filtered_articles, the_last_date, stop_sign = self.filter_articles(
                articles, pre_title
            )

            result.extend(self.format_articles(filtered_articles))

            if the_last_date != self.par_day or stop_sign:
                break

            next_controls = response.html.find(".action-bar a.btn.wide")
            if next_controls:
                url = self.get_next_page(next_controls)
            else:
                print(next_controls, "next_controls is false")
                break

        self.app_manger.write_log(
            f"看板 {self.board}，花費: {time.time() - start_time:.2f} 秒，共 {len(result)} 篇文章"
        )

        if result:
            data_txt = os.path.join(
                self.app_manger.data_dir, f"{self.board}.txt"
            ).replace("\\", "/")
            with open(data_txt, "+a", encoding="utf-8") as file:
                file.write(f"{result[0]['標題']}\n")

        return result

    def format_articles(self, articles):
        """格式化文章資料"""
        return [
            {
                "推文": article["push"],
                "標題": article["title"].translate(str.maketrans("", "", "[]")),
                "作者": article["author"],
                "日期": article["date"],
                "連結": article["link"],
            }
            for article in articles
        ]


# if __name__ == "__main__":
#     scraper = PttScraper("BaseballXXXX", 0, "today")
#     data = scraper.scrape()
#     formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
#     print(formatted_json)
