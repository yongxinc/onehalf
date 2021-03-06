# Generated by Django 3.1.5 on 2021-02-14 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MemberID', models.CharField(max_length=10)),
                ('Acc', models.CharField(max_length=30)),
                ('Pwd', models.CharField(max_length=15)),
                ('Name', models.CharField(max_length=30)),
                ('Tel', models.CharField(max_length=10)),
                ('Mail', models.EmailField(max_length=254)),
                ('LineRegistered', models.BooleanField()),
                ('LineID', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['MemberID'],
            },
        ),
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderNo', models.CharField(max_length=8)),
                ('BuyerID', models.CharField(max_length=8)),
                ('SellerID', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='UNIQLOItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UpdateDate', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('UNIQLOID', models.CharField(max_length=10)),
                ('UNIQLOTitle', models.CharField(max_length=20)),
                ('OriginalPrice', models.IntegerField(default=0)),
                ('ClothesColorJSON', models.CharField(default='黑色', max_length=500)),
                ('TitleImagesJSON', models.CharField(max_length=500)),
                ('SubImagesJSON', models.CharField(max_length=500)),
                ('ClothesType', models.CharField(choices=[('outer-casual-outer', '外套類-休閒/機能/連帽外套'), ('outer-jacket', '外套類-風衣/大衣/西裝外套'), ('outer-ultralightdown', '外套類-特級極輕羽絨服'), ('outer-down', '外套類-羽絨外套'), ('outer-fleece', '外套類-刷毛系列'), ('bottoms-long-pants', '下身類-休閒長褲'), ('bottoms-jeans', '下身類-牛仔褲'), ('bottoms-long-pants', '下身類-休閒長褲'), ('bottoms-easy-and-gaucho', '下身類-九分褲'), ('bottoms-leggings', '下身類-緊身褲/內搭褲'), ('bottoms-widepants', '下身類-寬褲'), ('bottom-skirt', '下身類-裙子'), ('tops-short-sleeves-and-tank-top', '上衣類-短袖/背心'), ('tops-short-long-and-3-4sleeves-and-cardigan', '上衣類-長袖/七分袖'), ('tops-shirts-and-blouses', '上衣類-襯衫'), ('tops-sweat-collection', '上衣類-休閒/連帽上衣‧連帽外套'), ('tops-flannel', '上衣類-法蘭絨系列'), ('tops-knit', '上衣類-針織衫/毛衣/開襟外套'), ('tops-dresses', '上衣類-洋裝‧連身褲')], default='outer-casual-outer', max_length=50)),
                ('Description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemNo', models.CharField(max_length=8)),
                ('Price', models.IntegerField()),
                ('Size', models.CharField(choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], default='XXS', max_length=3)),
                ('SellerImage', models.ImageField(upload_to='')),
                ('ExtendTimes', models.IntegerField()),
                ('ExpireDate', models.DateField()),
                ('ArrivalDate', models.DateField()),
                ('UNIQLOID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.uniqloitem')),
            ],
        ),
        migrations.CreateModel(
            name='Shippment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Addr', models.CharField(max_length=50)),
                ('Total', models.IntegerField()),
                ('DeliveryWay', models.CharField(choices=[('CONVENIENT_STORE', '店到店取貨付款'), ('FREIGHT', '貨運/郵寄')], default='CONVENIENT_STORE', max_length=30)),
                ('Status', models.CharField(choices=[('NOTSHIPPEDYET', '尚未寄出'), ('ONDELIVERY', '運送中'), ('ARRIVED', '已抵達，買家未取貨'), ('ORDERFINISHED', '訂單完成'), ('FAIL', '買家未取貨，交易失敗')], default='NOTSHIPPEDYET', max_length=50)),
                ('BuyerID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainsite.member')),
                ('OrderNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.salesrecord')),
            ],
            options={
                'ordering': ['OrderNo'],
            },
        ),
        migrations.AddField(
            model_name='salesrecord',
            name='ItemNo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainsite.stock'),
        ),
    ]
