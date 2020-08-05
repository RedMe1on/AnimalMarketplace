from django.contrib import admin

from .models import Categories, Owner, Product


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'h1', 'pub_date', 'parent')
    list_display_links = ('h1',)
    ordering = ('id',)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    readonly_fields = ('email')




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'h1', 'pub_date', 'parent', 'owner')
    list_display_links = ('h1',)
    list_filter = ('owner')
    search_fields = ('h1')
    ordering = ('id',)
    save_on_top = True
    save_as = True
    list_editable = ('h1')
    fieldsets = (
        (None, {
            'fields': ('h1')
        }),
    )
