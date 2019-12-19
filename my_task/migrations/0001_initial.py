# Generated by Django 2.1.2 on 2019-04-10 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskAcceptInfo',
            fields=[
                ('accept_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='领取编号')),
                ('task_id', models.CharField(max_length=10, verbose_name='任务编号')),
                ('user_id', models.CharField(max_length=10, verbose_name='领取者用户编号')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='领取时间')),
                ('end_time', models.DateTimeField(verbose_name='完成时间')),
                ('initiate_user_evaluate', models.SmallIntegerField(verbose_name='发起者星级评价')),
                ('accept_user_evaluate', models.SmallIntegerField(verbose_name='领取者星级评价')),
            ],
            options={
                'verbose_name_plural': '领取任务信息',
                'verbose_name': '领取任务信息',
                'db_table': 'task_accept',
            },
        ),
        migrations.CreateModel(
            name='TaskEvaluateInfo',
            fields=[
                ('evaluate_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='评价编号')),
                ('task_id', models.CharField(max_length=10, verbose_name='任务编号')),
                ('user_id', models.CharField(max_length=10, verbose_name='用户编号')),
                ('evaluate', models.CharField(max_length=1023, verbose_name='文本评价')),
                ('evaluate_time', models.DateTimeField(auto_now_add=True, verbose_name='评价时间')),
            ],
            options={
                'verbose_name_plural': '任务评价信息',
                'verbose_name': '任务评价信息',
                'db_table': 'task_evaluate',
            },
        ),
        migrations.CreateModel(
            name='TaskInfo',
            fields=[
                ('task_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='任务编号')),
                ('task_title', models.CharField(max_length=63, verbose_name='任务标题')),
                ('task_detail', models.CharField(max_length=1023, verbose_name='任务详情')),
                ('task_price', models.FloatField(verbose_name='任务赏金额度')),
                ('user_id', models.CharField(max_length=10, verbose_name='发起者用户编号')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='任务创建时间')),
                ('deadline', models.DateTimeField(verbose_name='任务截止时间')),
                ('task_status', models.DateTimeField(verbose_name='任务状态')),
            ],
            options={
                'verbose_name_plural': '任务信息',
                'verbose_name': '任务信息',
                'db_table': 'all_task',
            },
        ),
    ]
