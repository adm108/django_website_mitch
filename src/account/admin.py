from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):

    list_display = ('email', 'username', 'created_on', 'last_login',
                    'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('created_on', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
