from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户表
    """
    GENDER_TYPE = (
        ("male", "男"),
        ("female", "女"),
    )

    STATUS_TYPE = (
        ('ONLINE', "在线"),
        ('OFFLINE', "离线")
    )

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_TYPE, default="female", verbose_name="性别")
    location = models.CharField(max_length=30, null=True, blank=True, verbose_name="所在城市")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    avatar = models.CharField(max_length=50, null=True, blank=True, default="/static/img/default-avatar.png",
                              verbose_name="头像")
    status = models.CharField(max_length=6, choices=STATUS_TYPE, default="OFFLINE", verbose_name="在线状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    邮箱验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    email = models.EmailField(verbose_name="邮箱")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
