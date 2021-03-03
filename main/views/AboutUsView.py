from django.views.generic.base import TemplateView

class AboutUsView(TemplateView):
    template_name = "layouts/aboutUs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context