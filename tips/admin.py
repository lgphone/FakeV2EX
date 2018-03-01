from django.contrib import admin
from .models import Tips, TipsCategory

# Register your models here.


class TipsAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'category', 'title', 'author', 'add_time',)
    # 可以搜索的字段
    search_fields = ('title', )
    # 列出可以编辑的字段
    # list_editable = ('name', 'shop_price',)
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


class TipsCategoryAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'name', 'code', 'category_type', 'is_hot', 'add_time',)
    # 可以搜索的字段
    search_fields = ('name', )


admin.site.register(Tips, TipsAdmin)
admin.site.register(TipsCategory, TipsCategoryAdmin)