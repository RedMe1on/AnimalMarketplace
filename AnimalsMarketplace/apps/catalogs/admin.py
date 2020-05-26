from django.contrib import admin

from .models import Categories, Owner, Product


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'categories_title', 'pub_date')
    ordering = ('id',)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
