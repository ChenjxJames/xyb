# Generated by Django 2.1.2 on 2019-04-20 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_task', '0002_auto_20190420_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinfo',
            name='task_sex_preference',
            field=models.IntegerField(default=0, verbose_name='性别要求'),
        ),
    ]
