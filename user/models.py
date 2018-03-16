import uuid
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

    VERIFY_STATUS = (
        (0, "未验证"),
        (1, "已验证")
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_TYPE, default="female", verbose_name="性别")
    location = models.CharField(max_length=30, null=True, blank=True, default="", verbose_name="所在城市")
    mobile = models.CharField(max_length=11, null=True, blank=True, default="", verbose_name="电话")
    email = models.CharField(max_length=100, null=True, blank=True, default="", verbose_name="邮箱")
    email_verify = models.IntegerField(choices=VERIFY_STATUS, default=0, verbose_name="Email是否已经验证")
    mobile_verify = models.IntegerField(choices=VERIFY_STATUS, default=0, verbose_name="Mobile是否已经验证")
    avatar = models.CharField(max_length=50, null=True, blank=True, default="/static/img/default-avatar.png",
                              verbose_name="头像")
    session = models.CharField(max_length=50, null=True, blank=True, default="",
                               verbose_name="用户登录时会写入当前session_key")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    邮箱和手机验证码
    """
    VERIFY_CODE_TYPE = (
        (0, "Email"),
        (1, "Mobile")
    )
    code = models.CharField(max_length=10, verbose_name="验证码")
    to = models.CharField(max_length=30, verbose_name="发送给谁")
    code_type = models.IntegerField(choices=VERIFY_CODE_TYPE, default=0, verbose_name="验证码类型")
    task_id = models.CharField(max_length=37, null=True, blank=True, verbose_name="任务的返回id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "邮箱和手机验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.to


class UserFollowing(models.Model):
    """
    用户的Following 和 Block 关系表
    """
    CHOICES = (
        (-1, "None"),
        (0, "False"),
        (1, "True"),
    )

    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(UserProfile, verbose_name="关注那个用户", on_delete=models.CASCADE,
                                  related_name="following")
    is_following = models.IntegerField(choices=CHOICES, default=CHOICES[0][0], verbose_name="是否Following")
    is_block = models.IntegerField(choices=CHOICES, default=CHOICES[0][0], verbose_name="是否Block")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户的Following 和 Block 关系表"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'following',)

    def __str__(self):
        return self.user.username

    # 计算关注人数总数
    def count_following(self):
        return UserFollowing.objects.filter(user=self, is_following=1).count()

    # 计算被关注数量
    def count_follower(self):
        return UserFollowing.objects.filter(following=self, is_following=1).count()
