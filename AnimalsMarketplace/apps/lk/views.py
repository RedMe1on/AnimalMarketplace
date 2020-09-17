from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from .models import Profile


class ProfileViews(View):

    def get(self, request):
        return render(request, 'lk/profile.html')
