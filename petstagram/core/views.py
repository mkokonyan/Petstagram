from django.views import View


class PostOnlyView(View):
    form_class = None

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        pass

    def form_invalid(self, form):
        pass


class BootstrapFormMixin:
    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        self.__apply_bootstrap_classes(form)
        return form

    def __apply_bootstrap_classes(self, form):
        for (_, field) in form.fields.items():
            field.widget.attrs = {
                "class": "form-control",
            }
