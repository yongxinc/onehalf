# Generated by Django 3.1.5 on 2021-02-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uniqloitem',
            name='ClothesColorJSON',
            field=models.CharField(max_length=500),
        ),
    ]
