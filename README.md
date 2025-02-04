<div align="center" id="top"> 
<h1 align="center">PTT 熱門文章爬取與推送系統</h1>
</div>

<p align="center">
  <a href="#about">About</a> &#xa0; | &#xa0;
  <a href="#features">Features</a> &#xa0; | &#xa0;
  <a href="#requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#usage">Usage</a> &#xa0; | &#xa0;
  <a href="#code">Code</a> &#xa0; | &#xa0;
  <a href="#improvements">Improvements</a>
</p>

***

## About ##

> 爬取 PTT 各版當日熱門文章，並推送至指定的 Telegram 頻道或群組。內建關鍵字過濾機制，提高爬取效率，避免重複抓取。

***

## Features ##

- **爬取 PTT 熱門文章**：
  - 設定最低推文數門檻，僅保留高人氣文章。
  - 過濾指定關鍵字，以排除置底或無關內容。
- **推送至 Telegram**：
  - 爬取完成後，自動推送文章至指定的 Telegram 頻道或群組。
- **定期啟動**：
  - 自行選擇是否要打包成執行檔或是以 theads 定期啟動 `today_scheduler.py`

***

## Requirements ##

```bash
# Clone this project
$ git clone https://github.com/hsu27/ptt_crawler_today_articles.git
# Install dependencies
$ pip install -r requirements.txt
```

***

## Usage ##

1. **設定資料路徑**：
   - 修改 `utils/app_manager.py` 的 `init()` 內 `drive` 及 `sub_dir_path` 參數。

2. **關鍵字過濾設定**：
   - 編輯 `utils/app_manager.py` 內 `EXCLUDE_KEYWORDS`，確保排除不必要的關鍵字（置底須排除）。

3. **Telegram 推送設定**：
   - 於 `utils/app_manager.py` 設定 Telegram Bot token 及 Group/Channel ID。以及要爬取的看板及推文門檻。

4. **執行爬取**：
   ```bash
   python today_scheduler.py
   ```

***

## Code ##

### `PttScraper` 類別

- **`fetch_page(url)`**：發送請求取得 PTT 頁面 HTML 內容。
- **`parse_articles(elements)`**：解析文章資訊，包括標題、推文數、作者、日期、連結等。
- **`filter_articles(articles, pre_title)`**：過濾符合條件的文章，並檢查是否需要停止爬取。
- **`scrape()`**：主流程控制，從 PTT 版面開始爬取文章，遇到重複文章則停止。

### 打包執行檔
```bash
pip install pyinstaller
pyinstaller today_scheduler.spec
```
執行 `pyinstaller today_scheduler.spec` 來打包執行檔，並可配合工作排程器定期執行。

***

## Improvements ##

- **增加日期選擇功能**：目前僅支援當日文章，未來可擴展至自訂日期。
- **提升效率**：透過非同步請求加快爬取速度。

<br>
<a href="#top">Back to top</a>

<!-- use ctrl+shift+V to view this markdown on vscode -->

