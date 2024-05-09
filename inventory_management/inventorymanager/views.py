from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import AssetType

# Create your views here.
def LoginView(request):
    if request.method == "POST":
        pass
    else:
        return render(request,"inventorymanager/register.html")

class AssetView(generic.ListView) :
    template_name = "inventorymanager/overview.html"
    context_object_name = "atypes_list"

    def get_queryset(self) -> QuerySet[Any]:
        return AssetType.objects.all()