from .models import User, Band, Vote
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class AdminUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('user_id',
                           'full_name',
                           'password', 
                           'vote_finish',
                            )}),
        (_('Permissions'), {'fields': ('suffrage',
                                       'is_active', 
                                       'is_staff', 
                                       'is_superuser',
                                       'band',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('full_name',  'suffrage', 'vote_finish' ,'is_staff',)
    readonly_fields = ('user_id', 'full_name', 'vote_finish', 'last_login', 'date_joined')
    search_fields = ('full_name', )
    ordering = ('date_joined',)
    filter_horizontal = ('band',)
    actions = ['change_suffrage_true', 'change_suffrage_false', 'change_vote_finish_false'] 

    def change_suffrage_true(self, request, queryset):
        queryset.update(suffrage=True)
    change_suffrage_true.short_description = '選択された ユーザー に投票権を付与'

    def change_suffrage_false(self, request, queryset):
        queryset.update(suffrage=False)
    change_suffrage_false.short_description = '選択された ユーザー の投票権を剥奪'

    def change_vote_finish_false(self, request, queryset):
        queryset.update(vote_finish=False,
                        vote_contents=[]
                        )
    change_vote_finish_false.short_description = '選択された ユーザー の投票内容を削除'

@admin.register(Band)
class AdminBand(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
        # (_('Personal info'), {'fields': ()}),
        (_('他の設定'), {'fields': ('is_first_grade_band', )}),
    )
    list_display = ('name',  'is_first_grade_band',)
    actions = ['change_is_first_grade_band_true', 'change_is_first_grade_band_false']

    def change_is_first_grade_band_true(self, request, queryset):
        queryset.update(is_first_grade_band=True)
    change_is_first_grade_band_true.short_description = '選択された バンド を1年生バンドに設定'

    def change_is_first_grade_band_false(self, request, queryset):
        queryset.update(is_first_grade_band=False)
    change_is_first_grade_band_false.short_description = '選択された バンド を1年生バンドから除外'

@admin.register(Vote)
class AdminVote(admin.ModelAdmin):
    list_display = ('date_joined',  'is_work',)
    readonly_fields = ('date_joined',)

