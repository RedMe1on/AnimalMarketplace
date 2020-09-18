from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView, ListView, UpdateView
from django.shortcuts import get_object_or_404
from .forms import ProfileEditForm
from .models import Profile
from AnimalsMarketplace import settings


class ProfileViews(LoginRequiredMixin, DetailView):
    """Профиль"""
    login_url = settings.LOGIN_URL
    model = Profile
    template_name = 'lk/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile = self.model.objects.get_or_create(
            user=self.request.user,
            defaults={'name': self.request.user.username,
                      'email': self.request.user.email,
                      })
        return profile


class ProfileEditViews(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""
    model = Profile
    form_class = ProfileEditForm
    template_name_suffix = '_update'
    success_url = '/lk/profile'

    def get_object(self, queryset=None):
        profile = get_object_or_404(self.model, user=self.request.user)
        return profile
