from django.urls import path , include
from rest_framework import routers
from . import views
from django.views import generic

app_name = "inventorymanager"

urlpatterns = [
    path("",views.LoginView.as_view(),name="login"),
    path("register/",views.register,name="register"),
    path("settings/",generic.TemplateView.as_view(template_name="inventorymanager/settings.html")),
    path("newbase/",views.HomeView.as_view(),name='newbase'),
    path("editfield/<int:pk>/",views.editfield,name='editfield'),
    path("deletefield/<int:pk>/",views.deletefield,name='deletefield'),
    path("deleteallocated/<int:pk>/",views.deleteallocated,name='deleteallocated'),
    path('getfield/<int:record_id>/', views.getfield, name='getfield'),
    path('getallocatedfield/<int:record_id>/',views.getallocatedfield,name='getallocatedfield'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('newasset/',views.addfield,name='newasset'),
    path('allocated/',views.AllocatedView.as_view(),name='allocated'),
    path('newallocation',views.addfieldAllocated,name="newallocation"),
]