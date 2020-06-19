from django.shortcuts import render, get_object_or_404

from .models import Owner, Categories, Product


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)

        return render(request, self.template, context={self.model.__name__.lower(): obj})


class ObjectListMixin:
    model = None
    template = None

    def get(self, request):
        list_obj = self.model.objects.order_by('-pub_date')

        return render(request, self.template, context={f'list_{self.model.__name__.lower()}': list_obj})
