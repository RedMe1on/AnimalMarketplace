from django.http import Http404


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
        elif self.request.user.groups.all().filter(name='Модераторы'):
            return True
        else:
            return False

