from django.contrib import admin

# Register your models here.
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Отображение профиля в админке"""
    list_display = ('user', 'email',)
    # readonly_fields = ('email',)