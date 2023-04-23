from enum import Enum
from django.contrib.auth.models import User
from django.db import models

from apps.webapp.models.abstract_models import TimeStampAbstract
from apps.webapp.models.webapp_models import Country


class GenderEnum(Enum):
    UNKNOWN = 0
    MAN = 1
    WOMAN = 2
    SECRET = 3


class UserMember(TimeStampAbstract):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, help_text="会员")
    nickname = models.CharField(max_length=64, unique=True, db_index=True, help_text="用户昵称")
    phone = models.CharField(max_length=24, null=True, blank=True, help_text="联系电话")
    gender = models.IntegerField(
        default=0,
        choices=tuple([tag.value, tag.name] for tag in GenderEnum),
        help_text="性别"
    )

    class Meta:
        db_table = 'user_member'

    def __str__(self):
        return f'{self.user} - {self.nickname}'


class Address(TimeStampAbstract):
    # 地址簿
    user_member = models.ForeignKey(UserMember, on_delete=models.SET_NULL, null=True, help_text="会员")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, help_text='国家')
    zip_code = models.CharField(max_length=12, null=True, blank=True, help_text="邮编")
    name = models.CharField(max_length=64, help_text="姓名")
    phone = models.CharField(max_length=16, help_text='联系电话号码')
    province = models.CharField(max_length=36, null=True, blank=True, help_text="省份")
    city = models.CharField(max_length=36, null=True, blank=True, help_text="城市")
    district = models.CharField(max_length=48, null=True, blank=True, help_text="区")
    street = models.CharField(max_length=128, help_text="街道")
    note = models.CharField(max_length=36, help_text="地址备注")
    is_in_the_book = models.BooleanField(default=False, help_text="是否显示在地址簿中")
    is_delete = models.BooleanField(default=False, help_text="是否已经删除")

    class Meta:
        db_table = 'address'

    def __str__(self):
        return f'{self.user_member} - {self.country} - {self.name} - {self.zip_code}'
