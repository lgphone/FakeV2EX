from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from topic.models import Topic, TopicCategory

User = get_user_model()
# Create your models here.


class TopicVote(models.Model):
    """
    Topic 和 用户 关联表，信息
    """
    CHOICES = (
        (-1, "None"),
        (0, "False"),
        (1, "True"),
    )
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, verbose_name="Topic", on_delete=models.CASCADE)
    vote = models.IntegerField(choices=CHOICES, default=CHOICES[0][0], verbose_name="是否喜欢此贴")
    thanks = models.IntegerField(choices=CHOICES, default=CHOICES[0][0], verbose_name="是否感谢此贴")
    favorite = models.IntegerField(choices=CHOICES, default=CHOICES[0][0], verbose_name="是否收藏此贴")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = 'Topic和用户关联表'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'topic',)

    def __str__(self):
        return self.user.username


class FavoriteNode(models.Model):
    """
    用户和分类关联表，用于查询用户收藏的节点
    """
    CHOICES = (
        (-1, "None"),
        (0, "False"),
        (1, "True"),
    )
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    node = models.ForeignKey(TopicCategory, verbose_name="Topic", on_delete=models.CASCADE)
    favorite = models.IntegerField(choices=CHOICES, default=CHOICES[0][0], verbose_name="是否收藏此节点")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '用户和分类关联表'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'node',)

    def __str__(self):
        return self.user.username


class UserDetails(models.Model):
    """
    用户详情表
    """
    CHOICES_TYPE = (
        (0, "不展示"),
        (1, "展示")
    )

    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    website = models.CharField(max_length=50, null=True, blank=True, default="", verbose_name="个人网站")
    company = models.CharField(max_length=50, null=True, blank=True, default="", verbose_name="所在公司")
    company_title = models.CharField(max_length=50, null=True, blank=True, default="", verbose_name="工作职位")
    bio = models.CharField(max_length=300, null=True, blank=True, default="", verbose_name="个人简介")
    balance = models.IntegerField(default=500, verbose_name="财富值，默认500")
    show_balance = models.IntegerField(choices=CHOICES_TYPE, default=1, verbose_name="是否显示余额")
    list_rich = models.IntegerField(choices=CHOICES_TYPE, default=1, verbose_name="是否参与财富榜")
    my_home = models.CharField(max_length=30, null=True, blank=True, default="", verbose_name="登录后首页跳转")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserTopDu(models.Model):
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    top_du = models.IntegerField(default=0, verbose_name="活跃值")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="时间")

    class Meta:
        verbose_name = "用户活跃值"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'add_time',)

    def __str__(self):
        return self.user.username


class BalanceInfo(models.Model):
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    balance_type = models.CharField(max_length=30, verbose_name="类型")
    balance = models.IntegerField(verbose_name="数量")
    last_balance = models.IntegerField(default=500, verbose_name="目前余额")
    marks = models.CharField(max_length=200, verbose_name="备注")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="时间")

    class Meta:
        verbose_name = "用户账单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class SignedInfo(models.Model):
    """
    用户签到
    """
    CHOICES_TYPE = (
        (False, "未签到"),
        (True, "已经签到")
    )
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    status = models.BooleanField(choices=CHOICES_TYPE, verbose_name="是否签到")
    date = models.CharField(max_length=30, verbose_name="签到日期")
    signed_day = models.IntegerField(default=0, verbose_name="连续签到天数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="时间")

    class Meta:
        verbose_name = "用户签到"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'signed_day')

    def __str__(self):
        return self.user.username
