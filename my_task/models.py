from django.db import models


class TaskInfo(models.Model):
    """
    任务信息模型类
    """

    class Meta:
        db_table = 'all_task'
        verbose_name = '任务信息'
        verbose_name_plural = verbose_name

    task_id = models.CharField(max_length=10, null=False, verbose_name='任务编号', primary_key=True)
    task_title = models.CharField(max_length=63, null=False, verbose_name='任务标题')
    task_detail = models.CharField(max_length=1023, null=False, verbose_name='任务详情')
    task_price = models.FloatField(null=False, verbose_name='任务赏金额度')
    user_id = models.CharField(max_length=10, null=False, verbose_name='发起者用户编号')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='任务创建时间')
    deadline = models.DateTimeField(null=False, verbose_name='任务截止时间')
    task_sex_preference = models.SmallIntegerField(null=False, verbose_name='性别要求', default=0)
    task_status = models.SmallIntegerField(null=False, verbose_name='任务状态')
    # task_status = -1 or 0 or 1 or 2 or 3
    # -1:锁定； 0:待领取； 1:已领取待完成； 2:已完成； 3:过期。


class TaskAcceptInfo(models.Model):
    """
    领取任务信息模型类
    """

    class Meta:
        db_table = 'task_accept'
        verbose_name = '领取任务信息'
        verbose_name_plural = verbose_name

    accept_id = models.CharField(max_length=10, null=False, verbose_name='领取编号', primary_key=True)
    task_id = models.CharField(max_length=10, null=False, verbose_name='任务编号')
    user_id = models.CharField(max_length=10, null=False, verbose_name='领取者用户编号')
    start_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='领取时间')
    end_time = models.DateTimeField(null=True, verbose_name='完成时间')
    initiate_user_evaluate = models.SmallIntegerField(null=True, verbose_name='发起者星级评价')
    accept_user_evaluate = models.SmallIntegerField(null=True, verbose_name='领取者星级评价')
    # min_evaluate=0
    # max_evaluate=5


class TaskEvaluateInfo(models.Model):
    """
    任务评价信息模型类
    """

    class Meta:
        db_table = 'task_evaluate'
        verbose_name = '任务评价信息'
        verbose_name_plural = verbose_name

    evaluate_id = models.CharField(max_length=10, null=False, verbose_name='评价编号', primary_key=True)
    task_id = models.CharField(max_length=10, null=False, verbose_name='任务编号')
    user_id = models.CharField(max_length=10, null=False, verbose_name='用户编号')
    evaluate = models.CharField(max_length=1023, null=False, verbose_name='文本评价')
    evaluate_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='评价时间')
