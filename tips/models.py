from datetime import datetime
from django.db import models
from user.models import UserProfile
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class TipsCategory(models.Model):
    """
    Tips类别
    """
    CATEGORY_TYPE = (
        (1, "tab"),
        (2, "go"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    icon = models.CharField(null=True, blank=True, max_length=50, verbose_name="图标", help_text="图标")
    desc = models.TextField(null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat", on_delete=models.CASCADE)
    is_hot = models.BooleanField(default=False, verbose_name="是否最热", help_text="是否最热")
    avatar = models.CharField(max_length=50, null=True, blank=True, default="/static/img/default-avatar.png",
                              verbose_name="头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "Tips类别"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'category_type',)

    def __str__(self):
        return self.name


class Tips(models.Model):
    """
    Tips
    """
    category = models.ForeignKey(TipsCategory, verbose_name="Go分类", on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Tips作者", on_delete=models.CASCADE)
    tips_sn = models.CharField(max_length=50, default="", unique=True, verbose_name="Tips唯一货号")
    click_num = models.IntegerField(default=0, verbose_name="Tips点击数")
    like_num = models.IntegerField(default=0, verbose_name="顶数")
    dislike_num = models.IntegerField(default=0, verbose_name="踩数")
    title = models.TextField(max_length=120, verbose_name="Tips title")
    content = models.TextField(max_length=20000, verbose_name="Tips title")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = 'Tips'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
