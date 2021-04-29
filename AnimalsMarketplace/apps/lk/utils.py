from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet


class UnmoderatedObjectMixin:
    """Миксин для generic-view - Update/Delete
    Делает так, чтобы учитывались объекты, которые находятся на модерации, но не созданы
    еще в базе данных."""

    def get_object(self, queryset=None):
        unmoderated_object = self.get_unmoderated_object()
        if unmoderated_object:
            obj = unmoderated_object
        else:
            obj = super().get_object()
        return obj

    def get_unmoderated_object(self) -> QuerySet or False:
        """Получить объект на модерации, который не создан в db"""
        try:
            return self.model.unmoderated_objects.get(pk=self.kwargs.get('pk')).moderated_object.changed_object
        except ObjectDoesNotExist:
            return False