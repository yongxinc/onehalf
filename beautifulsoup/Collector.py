# 抓顏色與圖片

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import sys
import requests
import selenium
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, MetadataOptions
import json


class GoodsInfoCollector:
    def __init__(self, serialNumber):
        # 商品序號
        self.serialNumber = serialNumber
        self.colorDict = {}
        # 資料庫需要的資料

        self.title = ''
        self.type = ''
        self.colorList = ''
        self.titleImages = ''
        self.subImages = ''
        self.description = ''
        self.sizeTable = ''

        # 設定selenium
        Chrome_driver_path = 'C:/CodingProject/PythonProject/chromedriver/chromedriver.exe'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"')
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(
            executable_path=Chrome_driver_path, chrome_options=chrome_options)
        # driver.maximize_window()  # 最大化視窗

        goodspage = 'https://www.uniqlo.com/tw/store/goods/'+serialNumber
        driver.get(goodspage)
        self.goodssoup = BeautifulSoup(driver.page_source, "html.parser")

    def search(self):
        print('品名')
        self.title = self.getTitle()
        print('種類')
        self.type = self.getType()
        print('顏色列表')
        self.colorlist = self.getColorList()
        print('首圖')
        self.titleImages = self.getTitleImages()
        print('附圖')
        self.subImages = self.getSubImages()
        print('商品描述')
        self.discription = self.getDescription()

        self.save()

    def getTitle(self):

        result = self.goodssoup.find_all('h1', id='goodsNmArea')
        titleArray = []
        tmpStr = ''
        title = ''
        for g in result:
            tmpStr = g.text
            tmpStr = tmpStr.replace('女裝', '')
            titleArray = tmpStr.split(' ')
            for g in titleArray:
                title += g
        return title

    def getColorList(self):
        # 色塊圖片網址 https://im.uniqlo.com/images/tw/uq/pc/goods/433791/chip/50_433791.gif
        result = self.goodssoup.find_all('ul', id='listChipColor')
        for g in result:
            soup = g.find_all('img')
            for s in soup:
                tmp = str(s)
                tmp = tmp.replace('<img alt="', '')
                tmp = tmp.replace('" height="22" src="', '')
                tmp = tmp.replace(
                    'https://im.uniqlo.com/images/tw/uq/pc/goods/'+self.serialNumber + '/chip/', '')
                tmp = tmp.replace('_'+self.serialNumber +
                                  '.gif" width="22"/>', '')

                colorCode = tmp[-2:]
                color = tmp.replace(colorCode, '')
                colorDict[colorCode] = color  # 用來抓首圖
                colorListJSON = json.dumps(
                    self.colorDict, indent=4)  # 存進資料庫的資料是JSON
                # print(color, colorCode)
                return colorListJSON

        # print('color?')
        # print(colors)
        # 有顏色 就能抓到首圖

    # 獲取首圖

    def getTitleImages(self):
        tmplist = []
        for color in self.colorDict:
            tmplist.append('https://im.uniqlo.com/images/tw/uq/pc/goods/' +
                           self.serialNumber+'/item/'+color+'_'+self.serialNumber+'.jpg')
        titleimage_dict = {"title image": tmplist}
        titleimageJSON = json.dumps(titleimage_dict, indent=4)
        # print(titleimageJSON)
        return titleimageJSON

    # 獲取附圖#可能為空
    def getSubImages(self):
        result = self.goodssoup.find_all('ul', ['class', 'listimage clearfix'])
        tmp = ''
        unnecessarywords = '''<img '="" alt="商品照片" class="select" height="74" src="https://im.uniqlo.com/images/tw/uq/pc/img/l4/img_listimage_selected.gif" width="74"/>'''
        imagesArray = []
        for g in result:
            # 找到有img的內容
            imgs = g.find_all('img')
            # 針對每個img做處理
            for img in imgs:
                tmp = str(img)
                if tmp == unnecessarywords:
                    continue
                else:
                    # 把不需要的字除掉
                    tmp = tmp.replace('<img height="68" src="', '')
                    tmp = tmp.replace('" width="68"/>', '')
                    tmp = tmp.replace('_mini', '')
                    # 將處理好的圖片網址放進陣列中
                    imagesArray.append(tmp)
        image_dict = {"subimage": imagesArray}
        imageJSON = json.dumps(image_dict, indent=4)
        # print(imageJSON)
        return imageJSON

    def getDescription(self):
        result = self.goodssoup.find_all('p', id='shortComment')
        for g in result:
            tmp = str(g)
            tmp = tmp.replace(
                '<p class="readmore-js-section readmore-js-collapsed" id="shortComment" style="height: 99px;">', '')
            tmp = tmp.replace(
                '<p id="shortComment" style="display: none;"></p>', '')
            # print(tmp)
            return tmp

    # 獲得衣服種類(上衣、褲子、外套...)
    def getType(self):
        clothType = self.goodssoup.find_all('p', ['class', 'pathdetail'], 'a')
        clothTypeArray = []
        clothTypeStr = ""
        tmpStr = ""
        for g in clothType:
            tmpStr = g.text
            tmpStr = tmpStr.replace('\t', '')
            tmpStr = tmpStr.replace('\xa0', '')
            tmpStr = tmpStr.replace('/', '')
            clothTypeStr = tmpStr.replace('\n', '')
            clothTypeStr = clothTypeStr.replace('WOMEN⁄', '')
            clothTypeArray = clothTypeStr.split(" ")
        # print(clothTypeArray[0])
        return clothTypeArray[0]

    # 將爬到的資料寫進資料庫
    def save(self):
        unit = models.UNIQLOItem.create(
            UNIQLOID=self.serialNumber,
            UNIQLOTitile=self.title,
            OriginalPrice='299',
            ClothesColorJSON=self.colorList,
            TitleImagesJSON=self.titleImages,
            SubImagesJSON=self.subImages,
            ClothesType=self.type,
            Description=self.description
        )
        unit.save()  # 寫入資料庫


class SerialNumberCollector:
    def __init__(self):

        # 設定selenium
        Chrome_driver_path = 'C:/CodingProject/PythonProject/chromedriver/chromedriver.exe'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"')
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path=Chrome_driver_path, chrome_options=chrome_options)
        # driver.maximize_window()  # 最大化視窗

    def getSoup(self, suffix):
        page = 'https://www.uniqlo.com/tw/store/feature/women/'+suffix
        self.driver.get(page)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        return soup

    # casual-outer
    def findOuter(self):
        catagory = ['outer/casual-outer/',
                    'outer/jacket/', 'outer/ultralightdown/', 'outer/down', 'outer/fleece',
                    'bottoms/jeans/', 'bottoms/long-pants/', 'bottoms/easy-and-gaucho/', 'bottoms/leggings/', 'bottoms/widepants/',
                    'bottoms/short-and-half-pants/', 'bottom/skirt'
                    'tops/short-sleeves-and-tank-top/', 'tops/short-long-and-3-4sleeves-and-cardigan', 'tops/shirts-and-blouses',
                    'tops/sweat-collection', 'tops/flannel', 'tops/knit', 'tops/dresses']
        serialset = set()
        serialnum = ''
        for item in catagory:
            serialnum = ''
            result = self.getSoup(item)
            result = result.find_all(
                'dt', ['class', 'name'])
            for g in result:
                tmp = str(g)
                tmp = tmp.replace(
                    '<a href="https://www.uniqlo.com/tw/store/goods/', '')
                tmp = tmp.replace('<dt class="name">', '')
                for c in tmp:
                    try:
                        int(c)
                        serialnum += c
                    except:
                        serialnum += '/'
                        continue
            num = serialnum.split('/')

            for i in range(num.count('')):
                num.remove('')
            print(item)
            print(num)
            for n in num:
                serialset.add(n)

        return serialset
