from django.db import models

from apps.webapp.models import TimeStampAbstract


class Banner(TimeStampAbstract):
    BANNER_CACHE_KEY = 'SERVICE_ALL_BANNER'
    name = models.CharField(max_length=36, unique=True, help_text="名称")
    file_src = models.CharField(max_length=128, help_text='文件路径')
    index = models.IntegerField(default=0, help_text='排序')
    link_url = models.CharField(max_length=128, null=True, blank=True, help_text="链接URL")

    def __str__(self):
        return f'Name:{self.name};src={self.file_src};'

    class Meta:
        db_table = 'banner'
