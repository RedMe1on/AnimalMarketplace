from .models import Product, Categories


class ProductFilterMixin:

    def get_sex(self):
        """Список полов животного"""
        return Product.objects.filter(draft=False).distinct('sex')

    def get_breed(self):
        """Список пород"""
        return Product.objects.filter(draft=False).distinct('breed')

    def get_age(self):
        pass
