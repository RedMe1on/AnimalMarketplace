from .models import Product, Categories, RatingProduct


class ProductFilterMixin:

    def get_sex(self):
        """Список полов животного"""
        return Product.objects.filter(draft=False).distinct('sex')

    def get_breed(self):
        """Список пород"""
        return Product.objects.filter(draft=False).distinct('breed')

    def get_age(self):
        pass


class RatingProductMixin:
    model = None
    rating_model = None

    def get_user_rating(self, request, slug):
        ip = self.get_client_ip(request)
        user_rating = self.rating_model.objects.values_list('rating', flat=True).filter(
            product=self.model.objects.get(slug=slug), ip=ip)
        print(user_rating)
        return user_rating

    def get_avg_rating(self, slug: str) -> float:
        rating = self.rating_model.objects.filter(product=self.model.objects.get(slug=slug))
        star_list = [star.rating for star in rating]
        sum = 0
        for star in star_list:
            sum += star
        return round(sum / len(star_list), 1)

    @staticmethod
    def get_client_ip(request):
        """Получение ip адреса того, кто оставил рейтинг"""
        x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward_for:
            ip = x_forward_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
