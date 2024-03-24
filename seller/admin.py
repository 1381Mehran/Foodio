from django.contrib import admin

from .models import State, Seller


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('title',)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('get_user_phone', 'state', 'address', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('user__phone',)

    def get_user_phone(self, obj):
        return obj.user.phone

    get_user_phone.short_description = 'user phone'

