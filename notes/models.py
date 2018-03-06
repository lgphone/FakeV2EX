from datetime import datetime
from django.db import models
from user.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class NotesFolder(models.Model):
    """
    Notes 目录
    """
    title = models.CharField(default="", max_length=30, verbose_name="文件夹标题", help_text="文件夹标题")
    url = models.CharField(default="", max_length=30, unique=True, verbose_name="文件夹URL", help_text="文件夹URL")
    desc = models.TextField(null=True, blank=True, verbose_name="文件夹名称描述", help_text="文件夹名称描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "Notes 目录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Notes(models.Model):
    """
    Notes
    """
    NOTE_TYPE = (
        (0, "Default"),
        (1, "Markdown"),
    )

    folder = models.ForeignKey(NotesFolder, verbose_name="所在目录", default=1, on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Note作者", on_delete=models.CASCADE)
    notes_sn = models.CharField(max_length=20, unique=True, verbose_name="Note唯一sn")
    content = models.TextField(max_length=200000, null=True, blank=True, verbose_name="Note正文")
    notes_type = models.IntegerField(choices=NOTE_TYPE, verbose_name="Note正文类型", help_text="Note正文类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = 'Notes'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.notes_sn
