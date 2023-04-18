from enum import Enum
from django.contrib.auth.models import User
from django.db import models

from apps.webapp.models import TimeStampAbstract


class GenderEnum(Enum):
    UNKNOWN = 0
    MAN = 1
    WOMAN = 2
    SECRET = 3


GENDER_CLASSIFY = (
    (GenderEnum.UNKNOWN.value, '未知'),
    (GenderEnum.MAN.value, '男'),
    (GenderEnum.WOMAN.value, '女'),
    (GenderEnum.SECRET.value, '保密')
)


class UserMember(TimeStampAbstract):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, help_text="会员")
    nickname = models.CharField(max_length=64, unique=True, db_index=True, help_text="用户昵称")
    phone = models.CharField(max_length=24, null=True, blank=True, help_text="联系电话")
    gender = models.IntegerField(default=0, choices=GENDER_CLASSIFY, help_text="性别")

    class Meta:
        db_table = 'user_member'
