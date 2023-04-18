from django.db import models


class TimeStampAbstract(models.Model):
    """
    公共基类字段
    """
    create_at = models.DateTimeField(auto_now_add=True, help_text='创建日期')
    last_update = models.DateTimeField(auto_now=True, help_text='最新一次更新')

    class Meta:
        abstract = True
