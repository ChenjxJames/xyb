# Generated by Django 2.1.2 on 2019-04-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_user', '0003_auto_20190422_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='user_price',
            field=models.IntegerField(default=0, verbose_name='用户账户余额'),
        ),
    ]