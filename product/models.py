from django.utils.translation import gettext_lazy as _
from django.db import models


#######################################
#         Product Model Schema        #
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
        auto_now_add=True
    )

    class Meta:
        abstract = True


class ProductSchema(models.Model):
    pass


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
