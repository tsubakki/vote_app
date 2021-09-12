from .models import User, Band
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class AdminUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('user_id', 'username', 'full_name', 'password')}),
        # (_('Personal info'), {'fields': ()}),
        (_('Permissions'), {'fields': ('suffrage', 'is_active', 'is_staff', 'is_superuser',
                                       'band',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('full_name',  'suffrage', 'is_staff',)
    readonly_fields = ('user_id', 'username', 'full_name', 'last_login', 'date_joined')
    search_fields = ('full_name', )
    ordering = ('date_joined',)
    filter_horizontal = ('band',)
    actions = ['change_suffrage_true', 'change_suffrage_false'] 

    # 追加するアクションの関数
    def change_suffrage_true(self, request, queryset):
        queryset.update(suffrage=True)
    change_suffrage_true.short_description = '選択された ユーザー に投票権を付与'

    def change_suffrage_false(self, request, queryset):
        queryset.update(suffrage=False)
    change_suffrage_false.short_description = '選択された ユーザー の投票権を剥奪'

@admin.register(Band)
class AdminBand(admin.ModelAdmin):
    pass

