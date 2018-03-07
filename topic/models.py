from datetime import datetime
from django.db import models
from user.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class TopicCategory(models.Model):
    """
    Topic类别
    """
    CATEGORY_TYPE = (
        (1, "tab"),
        (2, "go"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    header_color = models.CharField(default="#001D25", max_length=30, verbose_name="头部颜色",
                                    help_text="头部颜色")
    desc = models.TextField(null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="node 类型", help_text="node 类型")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat", on_delete=models.CASCADE)
    is_hot = models.BooleanField(default=False, verbose_name="是否最热", help_text="是否最热")
    avatar = models.CharField(max_length=50, null=True, blank=True, default="/static/img/default-avatar.png",
                              verbose_name="头像")
    background_img = models.CharField(max_length=50, null=True, blank=True, default="/static/img/default-avatar.png",
                                      verbose_name="背景图片")
    theme_color = models.CharField(default="#001D25", max_length=30, verbose_name="主题颜色",
                                   help_text="主题颜色")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "Topic类别"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'category_type',)

    def __str__(self):
        return self.name

    # 计算所在分类的Topic数量
    @property
    def count_topic(self):
        return Topic.objects.filter(category=self).count()


class Topic(models.Model):
    """
    Topic
    """
    category = models.ForeignKey(TopicCategory, verbose_name="Go分类", on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Topic作者", on_delete=models.CASCADE)
    topic_sn = models.CharField(max_length=50, unique=True, verbose_name="Topic唯一sn")
    click_num = models.IntegerField(default=0, verbose_name="Topic点击数")
    title = models.TextField(max_length=120, verbose_name="Topic title")
    content = models.TextField(max_length=20000, null=True, blank=True, verbose_name="Topic content")
    html_content = models.TextField(max_length=20000, null=True, blank=True, verbose_name="Topic html content")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class NodeLink(models.Model):
    """
    Link
    """
    category = models.ForeignKey(TopicCategory, verbose_name="Node分类", on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Link作者", on_delete=models.CASCADE)
    title = models.CharField(default="", max_length=50, verbose_name="Link 标题")
    link = models.CharField(default="", max_length=50, unique=True, verbose_name="连接地址")
    desc = models.CharField(default="", max_length=120, verbose_name="Link 简介")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comments(models.Model):
    """
    Comments 评论表
    """
    topic = models.ForeignKey(Topic, verbose_name="Go分类", on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Topic作者", on_delete=models.CASCADE)
    content = models.TextField(max_length=20000, null=True, blank=True, verbose_name="Topic content")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = 'Comments'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.topic
