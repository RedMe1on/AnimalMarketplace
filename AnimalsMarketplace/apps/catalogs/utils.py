from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models import QuerySet, ObjectDoesNotExist
from moderation.helpers import automoderate

from .models import Product, ProductImage
from AnimalsMarketplace import settings


class ProductFilterMixin:

    def get_url(self):
        """Получение пути без домена"""
        return self.request.path

    def get_filter_product(self, queryset: QuerySet) -> QuerySet:
        """Фильтрация текущих товаров по выбранному фильтру"""
        filter_dict = {'is_visible': True}
        for k, v in self.request.GET.lists():
            if k == 'page':
                continue
            if k == 'image':
                filter_dict['additional_img' + '__image' + '__icontains'] = str('catalogs/product/')
                continue
            if k == 'price_start':
                if v[0] != '':
                    filter_dict['price__gte'] = v[0]
                continue
            if k == 'price_end':
                if v[0] != '':
                    filter_dict['price__lt'] = v[0]
                continue
            if v and len(v) == 1:
                filter_dict[str(k)] = str(v[0])
            else:
                filter_dict[str(k) + '__in'] = v
        queryset = queryset.filter(**filter_dict).distinct()
        return queryset


class ProductAutomodereteCUMixin:
    """Миксин, сочетающий в себе функции сохранения объявления и его картинок с автоматической модерацией"""

    def check_permission_for_automoderate(self):
        """Проверяет, является ли пользователь суперпользователем или модератором"""
        return self.request.user.is_superuser or self.request.user.groups.filter(
            name=settings.MODERATOR_GROUP_NAME).exists()

    @staticmethod
    def get_superuser():
        """Возвращает суперпользователя или создает его"""
        if User.objects.filter(is_superuser=True).exists():
            return User.objects.filter(is_superuser=True).first()
        else:
            return User.objects.create_superuser(username='admin', password='admin')

    def save_product(self, form, update=False) -> Product:
        """Сохранение объявления с модерацией"""
        new_product = form.save(commit=False)
        new_product.user = self.request.user
        if self.check_permission_for_automoderate():
            new_product.save()
            automoderate(new_product, self.request.user)
        elif update:
            new_product.save()
        else:
            # double save product for create object and send to moderate, need to think about how to fix it
            new_product.save()
            automoderate(new_product, self.get_superuser())
            new_product.save()
        return new_product

    def save_photo(self, product: Product, max_number_photo: int):
        """Сохранение изображений объявления с модерацией"""
        for photo in self.request.FILES.getlist('image')[:max_number_photo]:
            data = photo.read()
            image = ProductImage(product=product)
            if self.check_permission_for_automoderate():
                image.image.save(photo.name, ContentFile(data))
                automoderate(image, self.request.user)
            else:
                # double save product for create object and send to moderate, need to think about how to fix it
                image.image.save(photo.name, ContentFile(data))
                automoderate(image, self.get_superuser())
                image.image.save(photo.name, ContentFile(data))
