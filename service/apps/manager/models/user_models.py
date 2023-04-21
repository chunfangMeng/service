from django.contrib.auth.models import User
from django.db import models

from apps.member.models.user_models import GENDER_CLASSIFY
from apps.webapp.models.abstract_models import TimeStampAbstract


class ManagerUser(TimeStampAbstract):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, help_text="会员")
    nickname = models.CharField(max_length=64, unique=True, db_index=True, help_text="用户昵称")
    phone = models.CharField(max_length=24, null=True, blank=True, help_text="联系电话")
    gender = models.IntegerField(default=0, choices=GENDER_CLASSIFY, help_text="性别")

    class Meta:
        db_table = 'manager_user'
