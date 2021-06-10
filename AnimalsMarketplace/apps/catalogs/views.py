from django.db.models import QuerySet
from django.views.generic import ListView, DetailView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import MultipleObjectMixin
from django_filters.rest_framework import DjangoFilterBackend

from .forms import FilterForm, ReportForm
from .models import Categories, Product, BreedType
from .service import BreedTypeFilter
from .utils import ProductFilterMixin
from lk.models import Profile
from rest_framework.generics import ListAPIView
from .serializers import BreedTypeSerializers


class ProductList(ProductFilterMixin, FormView, ListView):
    """Отображение списка объявлений"""
    model = Product
    form_class = FilterForm
    paginate_by = 10
    ordering = ['-pub_date']

    def get_queryset(self):
        queryset = self.get_filter_product(super().get_queryset())
        return queryset


class MainPage(ProductList):
    """Отображение главной страницы"""
    template_name = 'catalogs/main.html'


class CategoriesList(ListView):
    """Отображение списка категорий"""
    model = Categories
    queryset = Categories.objects.order_by('-pub_date')


class CategoriesDetail(ProductFilterMixin, DetailView, FormView, MultipleObjectMixin):
    """Детальное отображение категории"""
    model = Categories
    form_class = FilterForm
    paginate_by = 10
    ordering = ['-pub_date']

    def get_context_data(self, **kwargs):
        object_list = self.get_filter_product(self.get_product_list_for_category())
        context = super().get_context_data(object_list=object_list.order_by('-pub_date'), **kwargs)
        return context

    def get_product_list_for_category(self) -> QuerySet:
        """Список товаров, которые относятся к дочерним и текущей категории"""
        parents_categories = self.object.get_descendants(include_self=True)
        list_product = Product.objects.filter(category__in=parents_categories)
        return list_product


class ProductDetail(DetailView, FormView):
    """Детальное отображение объявления"""
    model = Product
    form_class = ReportForm
    template_name = 'catalogs/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.object.user)
        return context


class BreedTypeListAPIView(ListAPIView):
    """API View for breed_type
    Отображение для доступа фронтенда к модели BreedType"""
    queryset = BreedType.objects.all()
    serializer_class = BreedTypeSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BreedTypeFilter


class ReportView(FormView):
    """Отображение жалобы"""
    template_name = 'catalogs/report.html'
    form_class = ReportForm
    success_url = '/report/success/'

    def form_valid(self, form):
        new_report = form.save(commit=False)
        new_report.product = Product.objects.get(id=self.kwargs.get('pk'))
        new_report.save()
        return super().form_valid(form)


class SuccessReportView(TemplateView):
    """Отображение успешного отправления жалобы"""
    template_name = 'catalogs/report_success.html'
