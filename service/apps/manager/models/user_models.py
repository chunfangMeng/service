from django.contrib.auth.models import User
from django.db import models

from apps.member.models import UserGenderChoices
from apps.webapp.models.abstract_models import TimeStampAbstract


class ManagerUser(TimeStampAbstract):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name="会员")
    nickname = models.CharField(max_length=64, unique=True, db_index=True, verbose_name="用户昵称")
    phone = models.CharField(max_length=24, null=True, blank=True, verbose_name="联系电话")
    gender = models.IntegerField(
        default=0,
        choices=UserGenderChoices.choices,
        help_text="性别"
    )

    class Meta:
        db_table = 'manager_user'

    def __str__(self):
        return f'User: {self.user} | Nickname:{self.nickname}'


class UserLoginLog(models.Model):
    # 用户登录日志记录
    class ClientChoices(models.IntegerChoices):
        CLIENT = 0
        MANAGEMENT = 1
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="会员")
    client = models.IntegerField(default=ClientChoices.CLIENT, choices=ClientChoices.choices, verbose_name='登录端')
    ip_address = models.CharField(max_length=16, db_index=True, verbose_name="IP地址")
    address = models.CharField(max_length=64, null=True, blank=True, verbose_name='登录地区')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')

    class Meta:
        db_table = 'user_login_log'

    def __str__(self):
        return f'{self.user} - {self.ip_address}'
