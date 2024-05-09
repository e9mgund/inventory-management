from django.urls import path , include
from rest_framework import routers
from . import views
from django.views import generic

app_name = "inventorymanager"

urlpatterns = [
    path("",views.AssetView.as_view()),
    path("login/",generic.TemplateView.as_view(template_name="inventorymanager/login.html")),
    path("register/",generic.TemplateView.as_view(template_name="inventorymanager/register.html"),name="register"),
    path("settings/",generic.TemplateView.as_view(template_name="inventorymanager/settings.html")),
    path("assettype/",generic.TemplateView.as_view(template_name="inventorymanager/assettype.html"),name="assettype"),
]