from django.shortcuts import render
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    template_name = "landing_page.html"

#
# def landing_page(request):
#     return render(request, "landing_page.html")
