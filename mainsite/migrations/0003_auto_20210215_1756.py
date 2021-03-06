# Generated by Django 3.1.5 on 2021-02-15 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_auto_20210215_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uniqloitem',
            name='ClothesType',
            field=models.CharField(choices=[('outer-casual-outer', '外套類-休閒/機能/連帽外套'), ('outer-jacket', '外套類-風衣/大衣/西裝外套'), ('outer-ultralightdown', '外套類-特級極輕羽絨服'), ('outer-down', '外套類-羽絨外套'), ('outer-fleece', '外套類-刷毛系列'), ('bottoms-long-pants', '下身類-休閒長褲'), ('bottoms-jeans', '下身類-牛仔褲'), ('bottoms-long-pants', '下身類-休閒長褲'), ('bottoms-easy-and-gaucho', '下身類-九分褲'), ('bottoms-leggings', '下身類-緊身褲/內搭褲'), ('bottoms-widepants', '下身類-寬褲'), ('bottom-skirt', '下身類-裙子'), ('tops-short-sleeves-and-tank-top', '上衣類-短袖/背心'), ('tops-short-long-and-3-4sleeves-and-cardigan', '上衣類-長袖/七分袖'), ('tops-shirts-and-blouses', '上衣類-襯衫'), ('tops-sweat-collection', '上衣類-休閒/連帽上衣‧連帽外套'), ('tops-flannel', '上衣類-法蘭絨系列'), ('tops-knit', '上衣類-針織衫/毛衣/開襟外套'), ('tops-dresses', '上衣類-洋裝‧連身褲'), ('default', '尚未分類')], default='default', max_length=50),
        ),
    ]
