from django.db import models


class UserInfo(models.Model):
    """
    用户信息模型类
    """

    class Meta:
        db_table = 'all_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    user_id = models.CharField(max_length=10, null=False, verbose_name='用户编号', primary_key=True)
    user_name = models.CharField(max_length=10, null=False, verbose_name='用户登录名', unique=True)
    user_password = models.CharField(max_length=32, null=False, verbose_name='用户登录密码')
    user_tel = models.CharField(max_length=11, null=False, verbose_name='用户手机号')
    user_sex = models.SmallIntegerField(null=False, verbose_name='用户性别')
    user_email = models.EmailField(max_length=255, null=False, verbose_name='用户邮箱地址')
    user_register_time = models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间')
    user_authorization = models.SmallIntegerField(null=False, verbose_name='用户权限', default=0)
    user_status = models.SmallIntegerField(null=False, verbose_name='用户账户状态', default=0)
    user_price = models.IntegerField(null=False, verbose_name='用户账户余额', default=0)