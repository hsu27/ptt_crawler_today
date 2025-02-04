import requests
from utils.ptt_scrape import PttScraper

# Telegram Bot Token
TOKEN = ""
# Chat Group ID，群組前要加-100
CHAT_ID = ""

# 設定不同看板的文章數量
BOARD_CONFIG = {
    "NBA": 70,
    "Baseball": 60,
    "C_Chat": 80,
    "PC_Shopping": 30,
    "Japan_Travel": 20,
    "creditcard": 30,
    "iOS": 20,
    "FAPL": 10,
    "BaseballXXXX": 20,
    "Military": 30,
    "basketballTW": 30,
    "HatePolitics": 50,
    "Lifeismoney": 50,
    "KoreaStar": 40,
    "FORMULA1": 5,
}


class SentMSG:

    def format_message(self, data, board, par_day):
        """將 JSON 轉為 Telegram 訊息格式（Markdown 版）"""
        sorted_data = sorted(
            data,
            key=lambda x: (100 if x["推文"] == "爆" else int(x["推文"])),
            reverse=True,
        )

        day = ''
        if par_day == 'today':
            day = '今日'
        else:
            day = '昨日'


        message = f"{day} {board}版熱門文章\n"
        for item in sorted_data:
            message += (
                f"{item['標題']}\n"
                f"推文數：{item['推文']}\t"
                f"[連結]({item['連結']})\n\n"
            )
        return message

    def send_telegram_message(self, message):
        """發送訊息到 Telegram"""
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }
        requests.post(url, json=payload)

    def scrape_and_send(self, board, limit, par_day):
        """爬取指定看板的熱門文章，並發送 Telegram 訊息"""
        scraper = PttScraper(board, limit, par_day)
        data = scraper.scrape()

        if data:
            msg = self.format_message(data, board, par_day)
            self.send_telegram_message(msg)

    def scrape_boards(self, par_day):
        """ 依據設定的 `BOARD_CONFIG` 爬取各個看板"""
        for board, limit in BOARD_CONFIG.items():
            self.scrape_and_send(board, limit, par_day)