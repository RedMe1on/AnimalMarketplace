from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from moderation.admin import ModerationAdmin

from .forms import ProductAdminForm
from .models import Categories, Product, ProductImage, BreedType, ReportModel
from django.contrib.admin.actions import delete_selected


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'seo_title', 'name', 'pub_date', 'parent')
    list_display_links = ('name',)
    fields = ('name', 'slug', 'seo_title', 'seo_description', 'image', 'parent', 'text',)
    ordering = ('id',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }


@admin.register(ReportModel)
class ReportModelAdmin(admin.ModelAdmin):
    list_display = ('cause', 'comment', 'product',)
    list_display_links = ('comment',)
    ordering = ('id',)


@admin.register(BreedType)
class BreedTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('name',)
    ordering = ('id',)


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


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category')


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, ModerationAdmin):
    resource_class = ProductResource
    list_display = ('id', 'name', 'pub_date', 'user', 'get_image', 'draft')
    readonly_fields = ('get_image',)
    list_per_page = 20
    list_display_links = ('name',)
    list_filter = ('user',)
    search_fields = ('name',)
    fields = (
        'name', 'seo_title', 'seo_description', 'user', 'category', 'sex', 'birthday', ('age', 'age_type'),
        ('breed', 'breed_type'), 'price', 'get_image', 'is_visible', 'draft', 'text')

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

    def get_image(self, obj):
        all_additional_img = obj.additional_img.all()
        if len(all_additional_img) != 0 and all_additional_img[0].image != '':
            if all_additional_img[0].image.url:
                return mark_safe(f'<img src={all_additional_img[0].image.url} width="50", height="50"')
        else:
            return mark_safe('Нет изображения')

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

    class Media:
        css = {
            "all": ("css/my_admin_styles.css",)
        }

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
