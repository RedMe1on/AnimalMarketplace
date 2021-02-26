from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db import models
from django.contrib import admin
from .models import Post, Categories, BlogTags


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pub_date', 'draft')
    list_display_links = ('name',)
    list_editable = ('draft',)
    search_fields = ('name',)
    exclude = ('views',)
    ordering = ('id',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()}
    }


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pub_date',)
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('id',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()}
    }


@admin.register(BlogTags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('id',)


