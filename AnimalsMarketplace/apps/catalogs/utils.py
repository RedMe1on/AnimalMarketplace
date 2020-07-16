from django.shortcuts import render, get_object_or_404


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)

        return render(request, self.template, context={self.model.__name__.lower(): obj})


class ObjectListMixin:
    model = None
    template = None

    def get(self, request):
        list_obj = self.model.objects.order_by('-pub_date')

        return render(request, self.template, context={f'list_{self.model.__name__.lower()}': list_obj})
