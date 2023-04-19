from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver

TITLE_SELECTOR = "h1.ytd-watch-metadata yt-formatted-string.ytd-watch-metadata"


def get_video_title(driver: WebDriver):
    # 取得頁面源代碼
    page_source = driver.page_source

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # 根據CSS選擇器選擇標題元素
    title_element = soup.select_one(TITLE_SELECTOR)

    # 檢查是否找到標題元素
    if title_element:
        return title_element.text
    else:
        return None


def save_html(driver: WebDriver, output_path="index.html"):
    # 獲取當前網頁的HTML內容
    html_content = driver.page_source

    # 將HTML內容寫入文件
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
