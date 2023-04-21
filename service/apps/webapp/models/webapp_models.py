from django.db import models
from enum import Enum

from apps.webapp.models.abstract_models import TimeStampAbstract


class ManagerDownload(TimeStampAbstract):
    class StatusEnum(Enum):
        INIT = 0
        PENNING = 1
        FAILED = 2
        SUCCESS = 3
    celery_task_id = models.CharField(max_length=32, db_index=True, help_text="后台下载任务id")
    file_path = models.CharField(max_length=128, help_text='文件保存路径')
    status = models.IntegerField(
        default=0,
        choices=tuple([tag.value, tag.name] for tag in StatusEnum),
        help_text="状态"
    )
    operator = models.CharField(max_length=150, help_text='操作人username')

    def __str__(self):
        return f'{self.celery_task_id};{self.status}'

    class Meta:
        db_table = 'manager_download'
