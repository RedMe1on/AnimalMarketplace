from django.contrib import admin

# Register your models here.
from lk.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # readonly_fields = ('email',)
    pass