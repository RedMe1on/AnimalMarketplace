from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView, FormView
from django.shortcuts import get_object_or_404, redirect
from moderation.helpers import automoderate

from .forms import ProfileEditForm, ProductForm, AdditionalImagesProductForm, ProductFormSet, \
    ModerationApproveRejectForm
from .models import Profile
from catalogs.models import Product, ProductImage
from .permissions import AuthorPermissionsMixin
from AnimalsMarketplace import settings


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
        queryset = super().get_queryset().filter(user=self.request.user).select_related()
        return queryset


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
        formset = ctx['formset']
        form_image = ctx['form_image']
        user = User.objects.filter(is_superuser=True)[0]
        if formset.is_valid() and form.is_valid() and form_image.is_valid():
            new_product = form.save(commit=False)
            new_product.user = self.request.user
            new_product.save()

            max_number = self.get_max_number()
            if max_number:
                for f in self.request.FILES.getlist('image')[:max_number]:
                    data = f.read()
                    image = ProductImage(product=new_product)
                    image.image.save(f.name, ContentFile(data))
                    automoderate(image, user)
                    image.image.save(f.name, ContentFile(data))
            for form in formset:
                form.save()
            for form in formset.deleted_forms:
                product_image = form.cleaned_data.get('id')
                product_image.delete()
            request = redirect(self.success_url)
            request.set_cookie('moderate', 'yes', max_age=2)
            return request
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_max_number(self) -> int:
        """Получает доступное количество загружаемых изображений"""
        number_of_img = self.object.additional_img.all().count()
        max_number = settings.MAX_UPLOAD_PHOTO
        sub = max_number - number_of_img
        if sub < 0:
            return False
        else:
            return sub

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['formset'] = ProductFormSet(self.request.POST, self.request.FILES, instance=self.object)
            ctx['form_image'] = AdditionalImagesProductForm(self.request.POST, self.request.FILES)
        else:

            ctx['formset'] = ProductFormSet(instance=self.object)
            ctx['form_image'] = AdditionalImagesProductForm()
        return ctx


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание объявления"""
    model = Product
    template_name = 'lk/product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('lk:product_list')

    def form_valid(self, form):
        ctx = self.get_context_data()
        form_image = ctx['form_image']
        user = User.objects.filter(is_superuser=True)[0]

        if form_image.is_valid() and form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = self.request.user
            # double save product for create object and send to moderate, need to think about how to fix it
            new_product.save()
            automoderate(new_product, user)
            new_product.save()

            for f in self.request.FILES.getlist('image')[:settings.MAX_UPLOAD_PHOTO]:
                data = f.read()
                image = ProductImage(product=new_product)
                # double save product for create object and send to moderate, need to think about how to fix it
                image.image.save(f.name, ContentFile(data))
                automoderate(image, user)
                image.image.save(f.name, ContentFile(data))

            request = redirect(self.success_url)
            request.set_cookie('moderate', 'yes', max_age=2)
            return request
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['form_image'] = AdditionalImagesProductForm(self.request.POST, self.request.FILES)
        else:
            ctx['form_image'] = AdditionalImagesProductForm()
        return ctx


class ModerationListViews(LoginRequiredMixin, ListView, FormView):
    model = Product
    template_name = 'lk/moderation_list.html'
    form_class = ModerationApproveRejectForm
    paginate_by = 10
    ordering = ['pub_date']

    def get_queryset(self):
        # queryset_image = ProductImage.
        queryset = self.model.unmoderated_objects.all()
        # qs1.union(qs2, qs3)
        return queryset


class ModerationDecisionViews(LoginRequiredMixin, FormView):
    form_class = ModerationApproveRejectForm
    template_name = 'lk/moderation_decision.html'
    success_url = reverse_lazy('lk:moderation')

    def form_valid(self, form):
        user = self.request.user
        unmoderated_product = Product.unmoderated_objects.get(pk=self.kwargs.get('pk'))
        additional_images = unmoderated_product.additional_img.all()

        if self.request.POST.get('approve'):
            unmoderated_product.moderated_object.approve(by=user, reason=self.request.POST['reason'])
            for additional_image in additional_images:
                additional_image.moderated_object.approve(by=user, reason=self.request.POST['reason'])
        elif self.request.POST.get('reject'):
            unmoderated_product.moderated_object.reject(by=user, reason=self.request.POST['reason'])
            for additional_image in additional_images:
                additional_image.moderated_object.reject(by=user, reason=self.request.POST['reason'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        unmoderated_product = Product.unmoderated_objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['product'] = unmoderated_product
        print(context)
        return context
