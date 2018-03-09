from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import VerifyCode
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'username', 'gender', 'email', 'location', 'status', 'avatar', 'is_active',)
    # 可以搜索的字段
    search_fields = ('name', )
    # 列出可以编辑的字段
    list_editable = ('gender', 'location', 'status')
    # 右侧过滤条件
    list_filter = ('add_time',)


# class VerifyCodeAdmin(admin.ModelAdmin):
#     # 要列出的字段
#     list_display = ('id', 'code', 'email',)
#     # 可以搜索的字段
#     search_fields = ('email', )
#     # 列出可以编辑的字段
#     list_editable = ('code',)
#     # 右侧过滤条件
#     list_filter = ('add_time',)


admin.site.register(User, UserAdmin)
# admin.site.register(VerifyCode, VerifyCodeAdmin)
