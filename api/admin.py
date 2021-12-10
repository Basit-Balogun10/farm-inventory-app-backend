from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import Account, Broiler, InventoryWeek


class AccountAdmin(UserAdmin):
    list_display = (
        'email', 'username', 'firstname', 'lastname', 'organization_name', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active',
    )
    search_fields = ('email', 'username', 'firstname', 'lastname', 'organization_name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = (
        'firstname', 'lastname', 'organization_name', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active')
    fieldsets = ()

    actions = ['activate_accounts', 'deactivate_accounts', ]

    def activate_accounts(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_accounts(self, request, queryset):
        queryset.update(is_active=False)


admin.site.register(Account, AccountAdmin)


@admin.register(Broiler)
class BroilerAdmin(admin.ModelAdmin):
    list_display = ('weight', 'feed', 'temperature', 'animal_bedding_date', 'date_of_birth', 'color', 'gender')
    list_filter = ('weight', 'feed', 'temperature', 'animal_bedding_date', 'date_of_birth', 'color', 'gender')
    search_fields = ('weight', 'feed', 'temperature', 'animal_bedding_date', 'date_of_birth', 'color', 'gender')


@admin.register(InventoryWeek)
class InventoryWeekAdmin(admin.ModelAdmin):
    list_display = ('broilers', 'is_concluded')
    list_filter = ('broilers', 'is_concluded')
    search_fields = ('broilers', 'is_concluded')
