from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from mainsite import models, forms
from django.contrib import auth
from django.contrib.auth import authenticate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import sys
import requests
import selenium
from bs4 import BeautifulSoup

import json


def index(request):
    if 'acc' in request.session:
        acc = request.session['acc']

    UQItems = models.UNIQLOItem.objects.all()
    UQItem_list = list()
    for _, UQItem in enumerate(UQItems):
        UQItem_list.append("{}".format(str(UQItem) + "<br>"))
    # return HttpResponse(UQItem_list)
    return render(request, 'index.html', locals())


def showgoods(request, id):
    if 'acc' in request.session:
        acc = request.session['acc']
    try:
        UQItem = models.UNIQLOItem.objects.get(UNIQLOID=id)
        if UQItem != None:
            return render(request, 'goodspage.html', locals())
    except:
        return redirect('/')


# member-seller-apply
def apply(request):
    if 'acc' in request.session:
        acc = request.session['acc']
    try:
        uniqlo_id = request.GET['uniqlo_id']
        itemexist = True
    except:
        uniqlo_id = 'None'
    return render(request, 'member/seller/apply.html', locals())

# member-login


def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            acc = form.cleaned_data['acc']
            pwd = form.cleaned_data['pwd']
            user1 = authenticate(username=acc, password=pwd)  # 驗證是否是會員
            if user1 is not None:  # 驗證通過
                isMember = True
            else:
                isMember = False
            message = '登入成功!'
        else:
            message = '登入失敗!'
    else:
        form = forms.LoginForm()

    try:
        if acc:
            request.session['acc'] = acc
    except:
        pass
    return render(request, 'member/login.html', locals())


def logout(request):
    if 'acc' in request.session:
        auth.logout(request)
    return HttpResponseRedirect('/')
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.


# member


def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            acc = form.cleaned_data['acc']
            pwd = form.cleaned_data['pwd']
            name = form.cleaned_data['name']
            tel = form.cleaned_data['tel']
            mail = form.cleaned_data['mail']

            if acc != None and pwd != None:
                member = models.Member(MemberID='流水號QQ', Acc=acc, Pwd=pwd, Name=name, Tel=tel,
                                       Mail=mail, LineRegistered=False, LineID='null')
                member.save()
                registered = True
            else:
                registered = False
            message = '註冊成功!'
        else:
            message = '註冊失敗!'
    else:
        form = forms.RegisterForm()

    return render(request, 'member/register.html', locals())


# member
def memberinfo(request):
    if 'acc' in request.session:
        acc = request.session['acc']
    return render(request, 'member/memberinfo.html', locals())

# 爬蟲


def collectInfo(request):
    if 'acc' in request.session:
        acc = request.session['acc']

    UQItems = models.UNIQLOItem.objects.all()
    UQItem_list = list()
    for _, UQItem in enumerate(UQItems):
        UQItem_list.append("{}".format(str(UQItem) + "<br>"))

    serialNumnCollector = SerialNumberCollector()
    serialset = serialNumnCollector.findOuter()
    print('已完成全部serialNumber的爬蟲')
    for n in serialset:
        if len(n) <= 4:
            continue
        else:
            goodsInfoCollector = GoodsInfoCollector(n)
            goodsInfoCollector.search()

    # goodsInfoCollector = GoodsInfoCollector('433245')
    # goodsInfoCollector.search()
    return render(request, 'index.html', locals())
# 爬蟲


class GoodsInfoCollector:
    def __init__(self, serialNumber):
        # 商品序號
        self.serialNumber = serialNumber
        self.colorDict = {}
        # 資料庫需要的資料
        self.typeDict = {('outer-casual-outer', '外套類-休閒外套'),
                         ('outer-jacket', '外套類-風衣/大衣/西裝外套'),
                         ('outer-ultralightdown', '外套類-特級極輕羽絨服'),
                         ('outer-down', '外套類-羽絨外套'),
                         ('outer-fleece', '外套類-fleece'),
                         ('bottoms-long-pants', '下身類-休閒長褲'),
                         ('bottoms-jeans', '下身類-牛仔褲'),
                         ('bottoms-long-pants', '下身類-休閒長褲'),
                         ('bottoms-easy-and-gaucho', '下身類-九分褲 ‧七分褲'),
                         ('bottoms-leggings', '下身類-緊身褲/內搭褲'),
                         ('bottoms-widepants', '下身類-寬褲'),
                         ('bottom-skirt', '下身類-裙子'),
                         ('tops-short-sleeves-and-tank-top', '上衣類-短袖/背心'),
                         ('tops-short-long-and-3-4sleeves-and-cardigan', '上衣類-長袖‧七分袖'),
                         ('tops-shirts-and-blouses', '上衣類-設計上衣‧襯衫'),
                         ('tops-sweat-collection', '上衣類-休閒/連帽上衣‧連帽外套'),
                         ('tops-flannel', '上衣類-法蘭絨系列'),
                         ('tops-knit', '上衣類-針織衫‧開襟外套'),
                         ('tops-dresses', '上衣類-洋裝‧連身褲')}

        self.title = ''
        self.type = ''
        self.colorListJSON = ''
        self.titleImages = ''
        self.subImages = ''
        self.description = ''
        self.sizeTable = ''
        self.price = ''

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
        print('目前正在搜尋', 'https://www.uniqlo.com/tw/store/goods/'+self.serialNumber)
        print('品名')
        self.title = self.getTitle()
        print('種類')
        self.type = self.getType()
        print('顏色列表')
        self.colorlistJSON = self.getColorList()
        print('首圖')
        self.titleImages = self.getTitleImages()
        print('附圖')
        self.subImages = self.getSubImages()
        print('商品描述')
        self.description = self.getDescription()
        print('價格')
        self.price = self.getPrice()
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
                self.colorDict[colorCode] = color  # 用來抓首圖
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
        print(clothTypeArray[0])
        for k, v in self.typeDict:
            if clothTypeArray[0] in v:
                return k
        return 'default'

        # return clothTypeArray[0]

    def getPrice(self):
        price = self.goodssoup.find_all('li', id='price')
        tmpStr = ''
        for g in price:
            tmpStr = g.text
            tmpStr = tmpStr.replace('<li class="price" id="price">', '')
            tmpStr = tmpStr.replace('NT$', '')
            tmpStr = tmpStr.replace('<span class="tax"></span></li>', '')
            tmpStr = tmpStr.replace('\xa0', '')
            tmpStr = tmpStr.replace(',', '')

        # print(price)
        return int(tmpStr)

    # 將爬到的資料寫進資料庫
    def save(self):
        unit = models.UNIQLOItem.objects.create(
            UNIQLOID=self.serialNumber,
            UNIQLOTitle=self.title,
            OriginalPrice=self.price,
            ClothesColorJSON=self.colorlistJSON,
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
