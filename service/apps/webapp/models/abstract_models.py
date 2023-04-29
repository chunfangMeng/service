from django.db import models


class TimeStampAbstract(models.Model):
    """
    公共基类字段
    """
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    last_update = models.DateTimeField(auto_now=True, verbose_name='最新一次更新')

    class Meta:
        abstract = True


class OperatorAbstract(models.Model):
    """
    操作人
    """
    founder = models.CharField(max_length=150, null=True, blank=True,
                               verbose_name="创建者", help_text="username in the User table")
    last_editor = models.CharField(max_length=150, null=True, blank=True,
                                   verbose_name="最后修改人", help_text="username in the User table")

    class Meta:
        abstract = True
