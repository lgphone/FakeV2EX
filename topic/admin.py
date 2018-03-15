from django.contrib import admin
from .models import Topic, TopicCategory, Comments, NodeLink

# Register your models here.


class TopicAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'category', 'title', 'author', 'click_num', 'add_time')
    # 可以搜索的字段
    search_fields = ('title', )
    # 列出可以编辑的字段
    list_editable = ('click_num', 'category',)
    # 右侧过滤条件
    list_filter = ('add_time',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30
    # 自定义显示隐藏字段
    # fieldsets = [
    #     (None, {'fields': ['name']}),
    #     ('完整信息', {'fields': ['name', 'shop_price', 'add_time', 'category'], 'classes': ['collapse']})
    # ]


class TopicCategoryAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'name', 'code', 'category_type', 'header_color', 'theme_color', 'add_time',)
    # 可以搜索的字段
    search_fields = ('name', 'code')
    # 列出可以编辑的字段
    list_editable = ('header_color', 'theme_color',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


class CommentsAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'topic', 'author', 'content', 'add_time',)
    # 可以搜索的字段
    search_fields = ('content', 'topic')
    # 列出可以编辑的字段
    list_editable = ('content',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


class NodeLinkAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'category', 'author', 'title', 'link', 'desc', 'add_time',)
    # 可以搜索的字段
    search_fields = ('title', 'link')
    # 列出可以编辑的字段
    list_editable = ('title', 'link', 'desc',)
    # 根据某个字段排序
    ordering = ('id',)
    # 分页，每页显示多少条
    list_per_page = 30


admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicCategory, TopicCategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(NodeLink, NodeLinkAdmin)
