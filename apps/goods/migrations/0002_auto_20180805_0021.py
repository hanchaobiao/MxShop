# Generated by Django 2.0.6 on 2018-08-05 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='shop_price',
            field=models.FloatField(default=0, help_text='本店价格', verbose_name='本店价格'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='sold_num',
            field=models.IntegerField(default=0, help_text='商品销售量', verbose_name='商品销售量'),
        ),
    ]
