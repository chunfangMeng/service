from django.contrib.auth.models import User
from django.db import models

from apps.member.models import UserGenderChoices
from apps.webapp.models.abstract_models import TimeStampAbstract, OperatorAbstract
from drf.permission import CUSTOM_PERMISSIONS


class ManagerUser(TimeStampAbstract):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name="会员")
    job_number = models.CharField(max_length=24, verbose_name="工号")
    nickname = models.CharField(max_length=64, unique=True, db_index=True, verbose_name="用户昵称")
    phone = models.CharField(max_length=24, null=True, blank=True, verbose_name="联系电话")
    gender = models.IntegerField(
        default=0,
        choices=UserGenderChoices.choices,
        help_text="性别"
    )

    class Meta:
        db_table = 'manager_user'
        permissions = CUSTOM_PERMISSIONS

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


class WebSite(TimeStampAbstract, OperatorAbstract):
    """
    网点
    """
    class SiteClassifyChoices(models.IntegerChoices):
        SELF_OPERATED = 0
        PROXY = 1
        FRANCHISEE = 2
    code = models.CharField(max_length=32, verbose_name="网点代码")
    name = models.CharField(max_length=64, verbose_name='网点名称')
    manager = models.CharField(max_length=150, verbose_name="负责人")
    classify = models.IntegerField(default=0, choices=SiteClassifyChoices.choices, verbose_name="网点类型")
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name="网点地址")
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name="网点联系方式")
    location = models.CharField(max_length=128, null=True, blank=True, verbose_name="地图地址")
    business_hours = models.CharField(max_length=48, verbose_name="营业时间")
    introduction = models.TextField(null=True, blank=True, verbose_name="网点介绍")
    sequence = models.IntegerField(default=0, verbose_name="排序[数字越大越靠前]")

    class Meta:
        db_table = 'web_site'
        ordering = ('sequence', '-id')

    def __str__(self):
        return f'{self.code} - {self.name}'


class ManagerWebSite(models.Model):
    """
    网点管理员关联
    """
    manager_user = models.ForeignKey(ManagerUser, on_delete=models.SET_NULL, null=True, verbose_name="管理员")
    web_site = models.ForeignKey(WebSite, on_delete=models.SET_NULL, null=True, verbose_name="网点")

    class Meta:
        db_table = 'manager_web_site'

    def __str__(self):
        return f'{self.manager_user} - {self.web_site}'
