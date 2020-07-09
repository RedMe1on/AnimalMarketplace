from django.contrib import admin

from .models import Categories, Owner, Product


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'h1', 'pub_date', 'parent')
    list_display_links = ('h1',)
    ordering = ('id',)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
