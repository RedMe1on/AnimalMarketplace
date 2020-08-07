from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin


from .models import Categories, Owner, Product, ProductImage


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'h1', 'pub_date', 'parent')
    list_display_links = ('h1',)
    ordering = ('id',)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    # readonly_fields = ('email',)
    pass


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'h1', 'pub_date', 'owner', 'image', 'draft')
    list_display_links = ('h1',)
    list_filter = ('owner',)
    search_fields = ('h1',)
    ordering = ('id',)
    form = ProductAdminForm
    save_on_top = True
    save_as = True
    inlines = [ProductImageInline]
    list_editable = ('draft',)
    # fieldsets = (
    #     (None, {
    #         'fields': ('h1',)
    #     }),
    # )
