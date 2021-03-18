import json
import sys
import requests
import selenium
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, MetadataOptions

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import sizeModel

serialNumber = "419912"

# # 獲得title、image
# authenticator = IAMAuthenticator(
#     'g5j4MrZ4AEZmVnlXg6klf_A-trxzpLdFwVuPoUrpHUhd')
# natural_language_understanding = NaturalLanguageUnderstandingV1(
#     version='2020-08-01',
#     authenticator=authenticator
# )

# natural_language_understanding.set_service_url(
#     'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2edcdaee-1d5c-4033-bc93-3ea5c167104e')


# response1 = natural_language_understanding.analyze(
#     url='https://www.uniqlo.com/tw/store/goods/'+serialNumber,
#     features=Features(metadata=MetadataOptions())).get_result()

# print(response1['metadata']['title'])
# print(response1['metadata']['image'])


# 設定selenium
Chrome_driver_path = 'C:/CodingProject/PythonProject/chromedriver/chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"')
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    executable_path=Chrome_driver_path, chrome_options=chrome_options)
driver.maximize_window()  # 最大化視窗

# # 用設定好的瀏覽器來獲取目標頁面
web = 'https://www.uniqlo.com/tw/store/goods/'+serialNumber
driver.get(web)
soup = BeautifulSoup(driver.page_source, "html.parser")

# 獲得衣服種類(上衣、褲子、外套...)
clothType = soup.find_all('p', ['class', 'pathdetail'], 'a')
clothTypeArray = []
clothTypeStr = ""
tmpStr = ""
for g in clothType:
    tmpStr = g.text
    tmpStr = tmpStr.replace('\t', '')
    tmpStr = tmpStr.replace('\xa0', '')
    tmpStr = tmpStr.replace('/', '')
    clothTypeStr = tmpStr.replace('\n', '')
clothTypeArray = clothTypeStr.split(" ")
# print(clothTypeArray)

# 抓取尺寸資訊
web = 'https://www.uniqlo.com/tw/store/support/size/'+serialNumber+'_size.html'
driver.get(web)
soup = BeautifulSoup(driver.page_source, "html.parser")

# 抓取尺寸資訊 # 抓取sizeHeaders
tmppp1 = ""
sizeHeaders = soup.find_all('th', ['class', 'header01'])
for g in sizeHeaders:
    tmppp1 += g.text + " "
sizeHeaders = tmppp1.split(' ')
# same as 'for i in range(len(list))'
r = range(len(sizeHeaders))
for i in sizeHeaders:
    if i == '':
        sizeHeaders.remove('')
# print('sizeHeaders')
# print(sizeHeaders)

# 抓取尺寸資訊 # 抓取sizeDetailHeaders
tmppp2 = ""
sizeDetailHeaders = soup.find_all('th')
for g in sizeDetailHeaders:
    tmppp2 += g.text + ' '
sizeDetailHeaders = tmppp2.split(' ')

# 移除抓到的尺寸資訊
for i in sizeDetailHeaders:
    if i == '':
        sizeDetailHeaders.remove('')
    for size in sizeHeaders:
        for i in sizeDetailHeaders:
            if i == size:
                sizeDetailHeaders.remove(size)

# 移除重複的欄位
hasMultiTables = False
uniquesizeDetailHeaders = []
for element in sizeDetailHeaders:
    if element not in uniquesizeDetailHeaders:
        uniquesizeDetailHeaders.append(element)
if len(uniquesizeDetailHeaders) != len(sizeDetailHeaders):
    hasMultiTable = True  # 表示有兩個table

sizeDetailHeaders = uniquesizeDetailHeaders

# print('sizeDetailHeaders')
# print(sizeDetailHeaders)

# 抓取尺寸資訊 # 抓取sizeDetailHeaders' sizeDetailInfos

tmppp3 = ''
sizeDetailInfos = soup.find_all('td', ['nowrap class', 'tdclass01'])
for g in sizeDetailInfos:
    tmppp3 += g.text + ' '
    # print(g.text)
sizeDetailInfos = tmppp3.split(' ')
# print('sizeDetailInfos')
# print(sizeDetailInfos)

# 將爬到的尺寸資訊(resultall)建成表格或model供資料庫儲存

cloth = sizeModel.Top('cloth',
                      sizeHeaders, sizeDetailHeaders, sizeDetailInfos, hasMultiTables)
cloth.processTables()
