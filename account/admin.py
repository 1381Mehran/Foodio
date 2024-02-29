from django.contrib import admin
from .models import User, CardNumber, UserWallet
from django.contrib.auth.models import Group

admin.site.unregister(Group)


class UserWalletInline(admin.TabularInline):
    model = UserWallet


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser')
    search_fields = ('phone', 'first_name', 'last_name')
    inlines = [UserWalletInline]


@admin.register(CardNumber)
class CardNumberAdmin(admin.ModelAdmin):
    list_display = ('get_user_phone', 'card_number', 'is_active')
    search_fields = ('card_number', 'user__phone')

    def get_user_phone(self, obj):
        return obj.user.phone

    get_user_phone.short_description = 'User Phone'
