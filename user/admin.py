from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    # 要列出的字段
    list_display = ('id', 'username', 'gender', 'email', 'avatar', 'is_active',)
    # 可以搜索的字段
    search_fields = ('name', )


admin.site.register(User, UserAdmin)
