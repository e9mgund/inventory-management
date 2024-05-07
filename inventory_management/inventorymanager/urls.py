from django.urls import path , include
from rest_framework import routers
from . import views
from django.views import generic

app_name = "tournament"

urlpatterns = [
    path("", generic.TemplateView.as_view(template_name="inventorymanager/base.html")),
]