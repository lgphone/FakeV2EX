from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import VerifyCode

User = get_user_model()

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'username', 'gender', 'email', 'location', 'session', 'avatar', 'is_active',)
    # 可以搜索的字段
    search_fields = ('name', )
    # 列出可以编辑的字段
    list_editable = ('gender', 'location',)
    # 右侧过滤条件
    list_filter = ('add_time',)


class VerifyCodeAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'code', 'to', 'add_time',)
    # 可以搜索的字段
    search_fields = ('to', )
    # 列出可以编辑的字段
    list_editable = ('code',)
    # 右侧过滤条件
    list_filter = ('add_time',)


admin.site.register(User, UserAdmin)
admin.site.register(VerifyCode, VerifyCodeAdmin)
