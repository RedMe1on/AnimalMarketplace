from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils.safestring import mark_safe

from .forms import ProductAdminForm
from .models import Categories, Product, ProductImage, RatingProduct
from django.contrib.admin.actions import delete_selected


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'h1', 'pub_date', 'parent')
    list_display_links = ('h1',)
    ordering = ('id',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }



@admin.register(RatingProduct)
class RatingAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('get_image',)
    extra = 3

    def get_image(self, obj):
        if obj.image == '':
            return mark_safe('Нет изображения')
        elif obj.image.url:
            return mark_safe(f'<img src={obj.image.url} width="50", height="50"')

    get_image.short_description = 'Изображение'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'h1', 'pub_date', 'profile', 'get_image', 'draft')
    readonly_fields = ('get_image',)
    list_display_links = ('h1',)
    list_filter = ('profile',)
    search_fields = ('h1',)
    ordering = ('id',)
    form = ProductAdminForm
    save_on_top = True
    save_as = True
    inlines = [ProductImageInline]
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }

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

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)

        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)

        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_premissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_premissions = ('change',)

    get_image.short_description = 'Изображение'


admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class FlatPagesAdmin(FlatPageAdmin):
    """Интерфейс простых страниц в админке"""
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }


admin.site.site_title = 'AnimalsMarketplace'
admin.site.site_header = 'AnimalsMarketplace'

delete_selected.short_description = 'Удалить выбранные'
