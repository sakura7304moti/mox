#Import-------------------------------------------------------------------------------
from io import StringIO, BytesIO
import os
import re
from time import sleep
import random
from urllib import request
import requests
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service
import datetime
import pandas as pd
import platform
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib
from urllib.parse import quote

from . import const

#--------------------------------------------------------------------------------------

def message(text: str):
    try:
        # 取得したTokenを代入
        line_notify_token = "bLg2L6w7MhUXm5eG1Pyz6jB5IJ8PVU3anYX5FbjUbSc"

        # 送信したいメッセージ
        message = text

        # Line Notifyを使った、送信部分
        line_notify_api = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        data = {"message": f"{message}"}
        requests.post(line_notify_api, headers=headers, data=data)
    except:
        pass
    
def get_driver(headless=True):
    options = ChromeOptions()
    if headless is True:
        print("Scraping on headless mode.")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")  # An error will occur without this line
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--headless")
    else:
        options.headless = False
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
    try:
        service=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options,service=service)
    except Exception as e:
        print('err -> ',e)
        driver = webdriver.Chrome(options=options)
    
    driver.get('https://twitter.com/home')
    cookie = const.get_cookie()
    for c in cookie:
        driver.add_cookie(c)
    driver.get('https://twitter.com/home')
    
    return driver

def get_url(query:str,since:str,until:str):
    parseQuery = urllib.parse.quote(query)
    url = f'https://twitter.com/search?q={parseQuery}since%3A{since}%20until%3A{until}%20min_faves%3A10&src=typed_query&f=live'
    return url


def generate_date_ranges( num_days:int, interval_days:int=5):
    date_ranges = []
    today = datetime.datetime.now()
    start_date = today - datetime.timedelta(days=num_days)
    while num_days > 0:
        end_date = start_date + datetime.timedelta(days=interval_days - 1)
        if end_date > datetime.datetime.now():
            end_date = datetime.datetime.now()
        date_range = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
        date_ranges.append(date_range)
        start_date = end_date + datetime.timedelta(days=1)
        num_days -= interval_days

    return date_ranges

#検索ワードと日数を指定してURLのリストを取得する関数
def get_urls(query:str,num_days:int, interval_days:int=5):
    date_ranges = generate_date_ranges(num_days,interval_days)
    urls = [get_url(query,rec[0],rec[1]) for rec in date_ranges]
    return urls


#todo ページからツイートを取得する関数
#todo ツイートから要素を取得する関数
#todo URL毎に実行される一番したまでスクロールしつつスクレイピングをする関数
#todo 一番スクレイピングの外側の関数 戻り値はTwitterQueryRecoardのリスト