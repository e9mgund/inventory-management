from django.urls import path , include
from rest_framework import routers
from . import views
from django.views import generic

app_name = "inventorymanager"

urlpatterns = [
    path("overview/",views.AssetTypeView.as_view(),name="overview"),
    path("login/",views.Login,name="login"),
    path("register/",views.register,name="register"),
    path("settings/",generic.TemplateView.as_view(template_name="inventorymanager/settings.html")),
    path("assets/",views.AssetsView.as_view(),name="assets"),
    path("employees/",views.EmployeesView.as_view(),name="employees"),
    path("new/",views.newFill,name="new"),
    path("newbase/",generic.TemplateView.as_view(template_name="inventorymanager/new_base.html"),name='newbase'),
]