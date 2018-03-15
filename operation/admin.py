from django.contrib import admin
from .models import TopicVote, FavoriteNode, UserDetails, UserTopDu, BalanceInfo, SignedInfo
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


class UserDetailsAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'website', 'company', 'balance', 'add_time',)
    # 可以搜索的字段
    search_fields = ('user', 'bio')
    # 列出可以编辑的字段
    list_editable = ('balance',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


class UserTopDuAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'top_du', 'add_time',)
    # 可以搜索的字段
    search_fields = ('user',)
    # 列出可以编辑的字段
    list_editable = ('top_du',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


class BalanceInfoAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'balance_type', 'balance', 'marks', 'last_balance', 'add_time',)
    # 可以搜索的字段
    search_fields = ('user',)
    # 列出可以编辑的字段
    list_editable = ('last_balance', 'marks',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


class SignedInfoAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'user', 'status', 'date', 'signed_day', 'add_time',)
    # 可以搜索的字段
    search_fields = ('user', 'date',)
    # 列出可以编辑的字段
    list_editable = ('status', 'signed_day',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


admin.site.register(TopicVote, TopicVoteAdmin)
admin.site.register(FavoriteNode, FavoriteNodeAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)
admin.site.register(UserTopDu,  UserTopDuAdmin)
admin.site.register(BalanceInfo, BalanceInfoAdmin)
admin.site.register(SignedInfo, SignedInfoAdmin)
