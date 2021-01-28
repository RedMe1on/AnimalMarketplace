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
            if k != 'page':
                if k == 'image':
                    if v == 'on':
                        filter_dict[str(k) + '__icontains'] = str('catalogs/product/')
                elif k == 'price_start':
                    if v[0] != '':
                        filter_dict['price__gte'] = v[0]
                elif k == 'price_end':
                    if v[0] != '':
                        filter_dict['price__lt'] = v[0]
                else:
                    if v and len(v) == 1:
                        filter_dict[str(k)] = str(v[0])
                    else:
                        filter_dict[str(k) + '__in'] = str(v)
        queryset = queryset.filter(**filter_dict)
        return queryset


class RatingProductMixin:
    model = None
    rating_model = None

    def get_user_rating(self, request, pk):
        """Получение ранее оставленного рейтинга по ip пользователя"""
        ip = self.get_client_ip(request)
        try:
            user_rating = self.rating_model.objects.get(product=self.model.objects.get(pk=pk), ip=ip)
            return user_rating.rating
        except ObjectDoesNotExist:
            return 0

    def get_avg_rating(self, pk: int) -> float:
        """Подсчет среднего рейтинга товара"""
        rating = self.rating_model.objects.filter(product=self.model.objects.get(pk=pk))
        star_list = [star.rating for star in rating]
        if star_list:
            sum = 0
            for star in star_list:
                sum += star
            return round(sum / len(star_list), 1)
        else:
            return 0

    @staticmethod
    def get_client_ip(request):
        """Получение ip адреса того, кто оставил рейтинг"""
        x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward_for:
            ip = x_forward_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
