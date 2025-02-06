from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class StartingPageView(TemplateView):
    template_name = "users/starting_page.html"