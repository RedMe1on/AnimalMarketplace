from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404, redirect

from .forms import ProfileEditForm, ProductForm, AdditionalImagesProductForm, ProductFormSet
from .models import Profile
from catalogs.models import Product, ProductImage
from .permissions import AuthorPermissionsMixin


class ProfileViews(LoginRequiredMixin, DetailView):
    """Профиль"""
    model = Profile
    template_name = 'lk/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile = self.model.objects.get(user=self.request.user)
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


class ProductListView(LoginRequiredMixin, ListView):
    """Список объявлений профиля"""
    model = Product
    template_name = 'lk/product_list.html'
    paginate_by = 10
    ordering = ['-pub_date']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ProductDeleteView(LoginRequiredMixin, AuthorPermissionsMixin, DeleteView):
    """Удалить объявление"""
    model = Product
    success_url = reverse_lazy('lk:product_list')
    template_name = 'lk/product_delete.html'


class ProductEditView(LoginRequiredMixin, AuthorPermissionsMixin, UpdateView):
    """Редактирование объявления"""
    model = Product
    template_name = 'lk/product_update.html'
    form_class = ProductForm
    success_url = reverse_lazy('lk:product_list')

    def form_valid(self, form):
        ctx = self.get_context_data()
        inlines = ctx['inlines']
        if inlines.is_valid() and form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = self.request.user
            new_product.save()
            for inline in inlines:
                new_formset = inline.save(commit=False)
                new_formset.product = new_product
                new_formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['inlines'] = ProductFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            ctx['inlines'] = ProductFormSet(instance=self.object)
        return ctx


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание объявления"""
    model = Product
    template_name = 'lk/product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('lk:product_list')

    def form_valid(self, form):
        ctx = self.get_context_data()
        inlines = ctx['inlines']
        if inlines.is_valid() and form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = self.request.user
            new_product.save()
            for f in self.request.FILES.getlist('additional_image')[:6]:
                data = f.read()
                image = ProductImage(product=new_product)
                image.additional_image.save(f.name, ContentFile(data))
                image.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['inlines'] = AdditionalImagesProductForm(self.request.POST, self.request.FILES)
        else:
            ctx['inlines'] = AdditionalImagesProductForm()
        return ctx

