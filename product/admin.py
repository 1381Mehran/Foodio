from django.contrib import admin
from .models import MainCat, MidCat, SubCat, Product, ProductImage, ProductProperty, Price


# Relating to categories

@admin.register(MainCat)
class MainCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    search_fields = ('title',)
    list_editable = ('is_active',)


@admin.register(MidCat)
class MidCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'is_active')
    search_fields = ('title',)
    list_editable = ('is_active',)


@admin.register(SubCat)
class SubCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'is_active')
    search_fields = ('title',)
    list_editable = ('is_active',)


# Relating to products

@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'item_type', 'item_name', 'item_detail', 'is_active')
    list_editable = ['item_type', 'is_active']
    search_fields = ['product_id', 'product_name', 'item_name']

    def product_id(self, obj):
        return obj.product.id

    product_id.short_description = 'Product ID'

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = 'Product Name'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'type', 'is_active')


class ProductPriceInline(admin.TabularInline):
    model = Price
    list_display = ('price', 'is_active')
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_info', 'category', 'is_active')
    search_fields = ('title', 'user_info')
    list_editable = ('is_active',)
    # inlines = [ProductPropertyInline, ProductImageInline]
    inlines = [ProductPriceInline]

    def user_info(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user.first_name and obj.user.last_name else \
            f'{obj.user.first_name}' if obj.user.first_name else f'{obj.user.last_name}' if obj.user.last_name else \
            obj.user.phone

    user_info.short_description = 'product owner'

