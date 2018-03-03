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
        return self.user

    # 计算顶的数量
    def count_like(self, topic_obj):
        return TopicVote.objects.filter(vote=1, topic=topic_obj).count()

    # 计算踩的数量
    def count_dislike(self, topic_obj):
        return TopicVote.objects.filter(vote=0, topic=topic_obj).count()

    # 计算收藏的数量
    def count_favorite(self, topic_obj):
        return TopicVote.objects.filter(favorite=1, topic=topic_obj).count()


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
        return self.user
