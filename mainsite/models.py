# -*-encoding: utf-8 -*-
from django.db import models
from datetime import datetime


class UNIQLOItem(models.Model):
    UpdateDate = models.DateTimeField('更新時間', auto_now=True)
    UNIQLOID = models.CharField(max_length=10)
    UNIQLOTitle = models.CharField(max_length=20)
    OriginalPrice = models.IntegerField(default=0)
    CLOTHES_TYPE_CHOICES = (
        ('outer-casual-outer', '外套類-休閒/機能/連帽外套'),
        ('outer-jacket', '外套類-風衣/大衣/西裝外套'),
        ('outer-ultralightdown', '外套類-特級極輕羽絨服'),
        ('outer-down', '外套類-羽絨外套'),
        ('outer-fleece', '外套類-刷毛系列'),
        ('bottoms-long-pants', '下身類-休閒長褲'),
        ('bottoms-jeans', '下身類-牛仔褲'),
        ('bottoms-long-pants', '下身類-休閒長褲'),
        ('bottoms-easy-and-gaucho', '下身類-九分褲'),
        ('bottoms-leggings', '下身類-緊身褲/內搭褲'),
        ('bottoms-widepants', '下身類-寬褲'),
        ('bottom-skirt', '下身類-裙子'),
        ('tops-short-sleeves-and-tank-top', '上衣類-短袖/背心'),
        ('tops-short-long-and-3-4sleeves-and-cardigan', '上衣類-長袖/七分袖'),
        ('tops-shirts-and-blouses', '上衣類-襯衫'),
        ('tops-sweat-collection', '上衣類-休閒/連帽上衣‧連帽外套'),
        ('tops-flannel', '上衣類-法蘭絨系列'),
        ('tops-knit', '上衣類-針織衫/毛衣/開襟外套'),
        ('tops-dresses', '上衣類-洋裝‧連身褲'),
        ('default', '尚未分類')
    )
    ClothesColorJSON = models.CharField(max_length=500)
    TitleImagesJSON = models.CharField(max_length=500)
    SubImagesJSON = models.CharField(max_length=2000)
    ClothesType = models.CharField(max_length=50,
                                   choices=CLOTHES_TYPE_CHOICES,
                                   default='default')

    Description = models.CharField(max_length=250)

    def __str__(self):
        return self.UNIQLOID + ' | ' + self.ClothesType + ' | ' + self.UNIQLOTitle

    class Meta:
        ordering = ['ClothesType', 'UNIQLOTitle']


class Stock(models.Model):
    ItemNo = models.CharField(max_length=8)
    UNIQLOID = models.ForeignKey(UNIQLOItem, on_delete=models.CASCADE)
    Price = models.IntegerField()
    SIZE_CHOICES = (
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'))

    Size = models.CharField(max_length=3,
                            choices=SIZE_CHOICES,
                            default='XXS')

    SellerImage = models.ImageField()
    ExtendTimes = models.IntegerField()
    ExpireDate = models.DateField()
    ArrivalDate = models.DateField()

    def __str__(self):
        return self.ItemNo


class SalesRecord(models.Model):
    OrderNo = models.CharField(max_length=8)  # 交易序號
    ItemNo = models.ForeignKey(
        Stock, on_delete=models.DO_NOTHING)  # 商品ID #FK
    BuyerID = models.CharField(max_length=8)
    SellerID = models.CharField(max_length=8)

    def __str__(self):
        return '銷售紀錄  OrderNo - {0}  '.format(self.OrderNo)


class Member(models.Model):
    MemberID = models.CharField(max_length=10)  # 系統產生
    Acc = models.CharField(max_length=30)  # 使用者輸入
    Pwd = models.CharField(max_length=15)
    Name = models.CharField(max_length=30)
    Tel = models.CharField(max_length=10)
    Mail = models.EmailField()
    LineRegistered = models.BooleanField()
    LineID = models.CharField(max_length=30)

    class Meta:
        ordering = ['MemberID']

    def __str__(self):
        return '{0} | {1}'.format(self.MemberID, self.Name)


class Shippment(models.Model):
    OrderNo = models.ForeignKey(SalesRecord, models.CASCADE)
    BuyerID = models.ForeignKey(
        Member, on_delete=models.DO_NOTHING)  # 買家會員ID #FK
    Addr = models.CharField(max_length=50)
    Total = models.IntegerField()

    DELIVERY_WAY_CHOICES = (
        ('CONVENIENT_STORE', '店到店取貨付款'),
        ('FREIGHT', '貨運/郵寄'))

    DeliveryWay = models.CharField(max_length=30,
                                   choices=DELIVERY_WAY_CHOICES,
                                   default='CONVENIENT_STORE')

    SHIPMENT_STATUS_CHOICES = (
        ('NOTSHIPPEDYET', '尚未寄出'),
        ('ONDELIVERY', '運送中'),
        ('ARRIVED', '已抵達，買家未取貨'),
        ('ORDERFINISHED', '訂單完成'),
        ('FAIL', '買家未取貨，交易失敗'))

    Status = models.CharField(max_length=50,
                              choices=SHIPMENT_STATUS_CHOICES,
                              default='NOTSHIPPEDYET')

    class Meta:
        ordering = ['OrderNo']

    def __str__(self):
        return '出貨紀錄 {0} ({1})'.format(self.OrderNo, self.DeliveryWay)
