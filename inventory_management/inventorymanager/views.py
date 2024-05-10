from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import AssetType , Assets

# Create your views here.
def LoginView(request):
    if request.method == "POST":
        pass
    else:
        return render(request,"inventorymanager/register.html")

class AssetTypeView(generic.ListView) :
    template_name = "inventorymanager/assettype.html"
    context_object_name = "atypes_list"

    def get_queryset(self) -> QuerySet[Any]:
        return AssetType.objects.all()

class AssetsView(generic.ListView):
    template_name = "inventorymanager/assets.html"
    context_object_name = "assets_list"

    def get_queryset(self) -> QuerySet[Any]:
        return Assets.objects.all()