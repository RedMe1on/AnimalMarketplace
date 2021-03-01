from django.db.models import QuerySet, ObjectDoesNotExist

from .models import Product


class ProductFilterMixin:

    def get_url(self):
        """Получение пути без домена"""
        return self.request.path

    def get_filter_product(self, queryset: QuerySet) -> QuerySet:
        """Фильтрация текущих товаров по выбранному фильтру"""
        filter_dict = {}
        for k, v in self.request.GET.lists():
            if k == 'page':
                continue
            if k == 'image':
                filter_dict[str(k) + '__icontains'] = str('catalogs/product/')
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
        queryset = queryset.filter(**filter_dict)
        return queryset


