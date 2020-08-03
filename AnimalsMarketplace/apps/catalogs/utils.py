from django.shortcuts import render, get_object_or_404, redirect, reverse


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

        return render(request, self.template, context={f'{self.model.__name__.lower()}_list': list_obj})


class ObjectUpdateMixin:
    model = None
    form_model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(request.POST, instance=obj)
        if bound_form.is_valid():
            edit_product = bound_form.save()
            return redirect(edit_product)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        product = self.model.objects.get(slug__iexact=slug)
        product.delete()
        return redirect(reverse(self.redirect_url))


