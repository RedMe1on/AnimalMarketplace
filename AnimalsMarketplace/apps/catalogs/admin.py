from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

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
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image == '':
            return mark_safe('Нет изображения')
        elif obj.image.url:
            return mark_safe(f'<img src={obj.image.url} width="50", height="50"')

    get_image.short_description = 'Изображение'


class ProductAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'h1', 'pub_date', 'owner', 'get_image', 'draft')
    readonly_fields = ('get_image',)
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
    #     ('None', {
    #         'fields': (('image', 'get_image'), )
    #     }),
    # )

    def get_image(self, obj):
        if obj.image == '':
            return mark_safe('Нет изображения')
        elif obj.image.url:
            return mark_safe(f'<img src={obj.image.url} width="50", height="50"')

    get_image.short_description = 'Изображение'


admin.site.site_title = 'AnimalsMarketplace'
admin.site.site_header = 'AnimalsMarketplace'
