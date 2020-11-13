from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import View

from .forms import ProfileEditForm, ProductForm
from .models import Profile
from catalogs.models import Product
from AnimalsMarketplace import settings


class ProfileViews(LoginRequiredMixin, DetailView):
    """Профиль"""
    login_url = settings.LOGIN_URL
    model = Profile
    template_name = 'lk/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile, created = self.model.objects.get_or_create(
            user=self.request.user,
            defaults={'name': self.request.user.username,
                      'email': self.request.user.email,
                      })
        return profile


class ProfileEditViews(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""
    model = Profile
    form_class = ProfileEditForm
    template_name = 'lk/profile_update.html'
    success_url = reverse_lazy('lk:profile')

    def get_object(self, queryset=None):
        profile = get_object_or_404(self.model, user=self.request.user)
        return profile


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удалить объявление"""
    model = Product
    success_url = reverse_lazy('lk:product_list')
    template_name = 'lk/product_delete.html'

    def get(self, request, *args, **kwargs):
        obj = self.get_object(queryset=None)
        profile = Profile.objects.get(user=self.request.user)
        if obj.profile == profile:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse(404)


class ProductListView(LoginRequiredMixin, ListView):
    """Список объявлений профиля"""
    model = Product
    template_name = 'lk/product_list.html'
    paginate_by = 10
    ordering = ['-pub_date']

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        queryset = super().get_queryset().filter(profile=profile)
        return queryset


class ProductEditView(LoginRequiredMixin, UpdateView):
    """Редактирование объявления"""
    model = Product
    template_name = 'lk/product_update.html'
    form_class = ProductForm
    success_url = reverse_lazy('lk:product_list')

    def get(self, request, *args, **kwargs):
        obj = self.get_object(queryset=None)
        profile = Profile.objects.get(user=self.request.user)
        if obj.profile == profile:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse(404)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание объявления"""
    model = Product
    template_name = 'lk/product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('lk:product_list')

    def form_valid(self, form):
        new_product = form.save(commit=False)
        new_product.profile = Profile.objects.get(user=self.request.user)
        new_product.save()
        return redirect(self.success_url)
