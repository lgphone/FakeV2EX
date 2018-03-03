from django.contrib import admin
from .models import TopicVote, FavoriteNode
# Register your models here.


class TopicVoteAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'user', 'topic', 'vote', 'thanks', 'favorite', 'add_time',)
    # 可以搜索的字段
    search_fields = ('user', 'topic')
    # 列出可以编辑的字段
    list_editable = ('thanks', 'vote', 'favorite')
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


class FavoriteNodeAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'user', 'node', 'favorite', 'add_time',)
    # 可以搜索的字段
    search_fields = ('user', 'node')
    # 列出可以编辑的字段
    list_editable = ('favorite',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


admin.site.register(TopicVote, TopicVoteAdmin)
admin.site.register(FavoriteNode, FavoriteNodeAdmin)
