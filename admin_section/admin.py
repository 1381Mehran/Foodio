from django.contrib import admin
from .models import Admin, Staff


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'is_active', 'created_at')
    search_fields = ('user', 'position')
    list_editable = ('is_active',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'admin', 'is_active', 'created_at')
    search_fields = ('user', 'position')
    list_editable = ('is_active',)
