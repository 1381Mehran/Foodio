from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import datetime


#######################################
#    Product Category Model Schema    #
#######################################


class ProductCategorySchema(models.Model):

    title = models.CharField(
        _('title'),
        max_length=100,
    )

    active = models.BooleanField(
        _('active'),
        default=True
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


class MainCat(ProductCategorySchema):

    class Meta:
        db_table = 'main_categories'
        verbose_name = _('Main Category')
        verbose_name_plural = _('Main Categories')


class MidCat(ProductCategorySchema):
    parent = models.ForeignKey(
        MainCat,
        on_delete=models.CASCADE,
        verbose_name=_('Mid Category'),
        related_name='mid_cats'
    )

    class Meta:
        db_table = 'mid_categories'
        verbose_name = _('Mid Category')
        verbose_name_plural = _('Mid Categories')


class SubCat(ProductCategorySchema):
    parent = models.ForeignKey(
        MidCat,
        on_delete=models.CASCADE,
        verbose_name=_('Sub Category'),
        related_name='sub_cats'
    )

    class Meta:
        db_table = 'sub_categories'
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')


#######################################
#       Products Models Schema        #
#######################################

class Product(models.Model):
    title = models.CharField(
        _('title')
        , max_length=450
    )
    category = models.ForeignKey(
        SubCat,
        on_delete=models.CASCADE,
        related_name='product_categories',
        verbose_name=_('Sub Category')
    )

    introduce = models.TextField(
        _('introduce'),
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
