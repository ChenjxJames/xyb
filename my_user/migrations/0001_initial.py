# Generated by Django 2.1.2 on 2019-04-10 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='用户编号')),
                ('user_name', models.CharField(max_length=10, unique=True, verbose_name='用户登录名')),
                ('user_password', models.CharField(max_length=32, verbose_name='用户登录密码')),
                ('user_tel', models.CharField(max_length=11, verbose_name='用户手机号')),
                ('user_sex', models.CharField(max_length=1, verbose_name='用户性别')),
                ('user_email', models.EmailField(max_length=255, verbose_name='用户邮箱地址')),
                ('user_register_time', models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间')),
                ('user_authorization', models.IntegerField(default=0, verbose_name='用户权限')),
                ('user_status', models.IntegerField(default=0, verbose_name='用户账户状态')),
            ],
            options={
                'verbose_name_plural': '用户信息',
                'verbose_name': '用户信息',
                'db_table': 'all_user',
            },
        ),
    ]