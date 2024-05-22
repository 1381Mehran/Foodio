from django.utils.translation import gettext_lazy as _
from django.db import models

from account.models import User
from seller.models import Seller


#######################################
#    Product Category Model Schema    #
#######################################


class ProductCategorySchema(models.Model):

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    title = models.CharField(
        _('title'),
        max_length=100,
    )

    is_active = models.BooleanField(
        _('is active'),
        default=False
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        editable=False
    )

    class Meta:
        abstract = True


#######################################
#                 END                 #
#######################################


# class MainCat(ProductCategorySchema):
#
#     class Meta:
#         db_table = 'main_categories'
#         verbose_name = _('Main Category')
#         verbose_name_plural = _('Main Categories')
#
#     def __str__(self):
#         return self.title
#
#
# class MidCat(ProductCategorySchema):
#     parent = models.ForeignKey(
#         MainCat,
#         on_delete=models.CASCADE,
#         verbose_name=_('Main Category'),
#         related_name='mid_cats'
#     )
#
#     class Meta:
#         db_table = 'mid_categories'
#         verbose_name = _('Mid Category')
#         verbose_name_plural = _('Mid Categories')
#
#     def __str__(self):
#         return self.title
#
#
# class SubCat(ProductCategorySchema):
#     parent = models.ForeignKey(
#         MidCat,
#         on_delete=models.CASCADE,
#         verbose_name=_('Mid Category'),
#         related_name='sub_cats'
#     )
#
#     class Meta:
#         db_table = 'sub_categories'
#         verbose_name = _('Sub Category')
#         verbose_name_plural = _('Sub Categories')
#
#     def __str__(self):
#         return self.title

class ProductCategory(ProductCategorySchema):

    class Meta:
        db_table = 'categories'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title

#######################################
#       Products Models Schema        #
#######################################


class Product(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        verbose_name=_('Seller'),
        related_name='products',
    )

    title = models.CharField(
        _('title')
        , max_length=450
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('Category')
    )

    introduce = models.TextField(
        _('introduce'),
        null=True,
        blank=True
    )

    stock = models.PositiveIntegerField(
        _('stock'),
        default=0
    )

    celery_task_id = models.CharField(
        verbose_name=_('celery_task_id'),
        max_length=256,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        _('is active'),
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'), editable=False)

    class Meta:
        db_table = 'Products'
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Price(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
        related_name='prices'
    )

    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_('Price'))

    is_active = models.BooleanField(default=False, verbose_name=_('is active'))

    def __str__(self):
        return f"{self.product.title} - {self.price}"


class ProductImage(models.Model):

    class ImageType(models.TextChoices):
        BANNER = 'banner', 'Banner'
        SUB = 'sub', 'Sub'

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images',
        verbose_name=_('product')
    )
    image = models.ImageField(
        upload_to=f'images/product',
        verbose_name=_('image')
    )
    type = models.CharField(
        _('type'),
        choices=ImageType.choices,
        default=ImageType.SUB,
        max_length=6
    )

    is_active = models.BooleanField(
        _('is active'),
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'), editable=False)

    class Meta:
        db_table = 'product_images'
        verbose_name = 'image'
        verbose_name_plural = _('images')


class ProductProperty(models.Model):
    class PropertyType(models.TextChoices):
        PROPERTY = 'property', 'Property'
        SPECIFICATION = 'specification', 'Specification'

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_properties',
        verbose_name=_('product')
    )
    item_type = models.CharField(
        _('item type'),
        choices=PropertyType.choices,
        max_length=14
    )
    item_name = models.CharField(
        _('item name'),
        max_length=50,
    )
    item_detail = models.CharField(
        _('item detail'),
        max_length=300
    )

    is_active = models.BooleanField(
        _('is active'),
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'), editable=False)

    class Meta:
        db_table = 'Product_properties'
        verbose_name = 'Product property'
        verbose_name_plural = _('Product properties')
