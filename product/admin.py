from django.contrib import admin
from .models import MainCat, MidCat, SubCat


@admin.register(MainCat)
class MainCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'active')
    search_fields = ('title',)
    list_editable = ('active',)


@admin.register(MidCat)
class MidCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'active')
    search_fields = ('title',)
    list_editable = ('active',)


@admin.register(SubCat)
class SubCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'active')
    search_fields = ('title',)
    list_editable = ('active',)
