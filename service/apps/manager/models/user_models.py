from django.contrib.auth.models import User
from django.db import models

from apps.member.models import GenderEnum
from apps.webapp.models.abstract_models import TimeStampAbstract


class ManagerUser(TimeStampAbstract):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name="会员")
    nickname = models.CharField(max_length=64, unique=True, db_index=True, verbose_name="用户昵称")
    phone = models.CharField(max_length=24, null=True, blank=True, verbose_name="联系电话")
    gender = models.IntegerField(
        default=0,
        choices=tuple([tag.value, tag.name] for tag in GenderEnum),
        help_text="性别"
    )

    class Meta:
        db_table = 'manager_user'

    def __str__(self):
        return f'User: {self.user} | Nickname:{self.nickname}'
