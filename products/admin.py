from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    '''
    Selects which details will be shown in the Django admin
    '''
    list_display = (
      'p_id',
      'name',
      'category',
      'price',
      'rating',
      'image',
    )

    # Items are ordered in admin by category first then alphabetically by name
    ordering = ('category', 'name')


class CategoryAdmin(admin.ModelAdmin):
    '''
    Selects which details will be shown in the Django admin
    '''
    list_display = (
      'friendly_name',
      'name',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
