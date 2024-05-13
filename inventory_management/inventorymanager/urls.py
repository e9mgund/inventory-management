from django.urls import path , include
from rest_framework import routers
from . import views
from django.views import generic

app_name = "inventorymanager"

urlpatterns = [
    path("",views.AssetTypeView.as_view(),name="overview"),
    path("login/",generic.TemplateView.as_view(template_name="inventorymanager/login.html")),
    path("register/",generic.TemplateView.as_view(template_name="inventorymanager/register.html"),name="register"),
    path("settings/",generic.TemplateView.as_view(template_name="inventorymanager/settings.html")),
    path("assets/",views.AssetsView.as_view(),name="assets"),
    path("employees/",views.EmployeesView.as_view(),name="employees"),
    path("new/",views.newFill,name="new"),
]