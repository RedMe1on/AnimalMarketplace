from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.generic import CreateView

from .models import Mailing
from .forms import MailingForm


class MailingView(CreateView):
    model = Mailing
    success_url = '/mailing/thanks'
    form_class = MailingForm
    template_name = 'mailing/mailing.html'

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return render(self.request, self.template_name, context={'form': form})


class ThanksView(TemplateView):
    template_name = 'mailing/thanks.html'
