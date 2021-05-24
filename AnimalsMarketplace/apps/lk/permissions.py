from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from AnimalsMarketplace import settings
from .models import Profile


class PhoneNumberPermissionsMixin:
    """Миксин для блокирования личного кабинета, если у пользователя не введен номер телефона для объявлений"""

    def has_permissions(self):
        profile = Profile.objects.get(user=self.request.user)
        if profile.phone_number_ads:
            return True
        else:
            return False

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return redirect(reverse('lk:edit_profile'))
        return super().dispatch(request, *args, **kwargs)


class AuthorPermissionsMixin:
    """Миксин для проверки авторства для редактирования объявлений"""

    def has_permissions(self):
        return self.get_object().user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class ModeratePermissionsMixin(AuthorPermissionsMixin):
    """Миксин для проверки прав на редактирование объявлений модерации"""

    def has_permissions(self):
        if self.request.user.is_superuser:
            return True
        elif self.request.user.groups.filter(name=settings.MODERATOR_GROUP_NAME).exists():
            return True
        else:
            return False
