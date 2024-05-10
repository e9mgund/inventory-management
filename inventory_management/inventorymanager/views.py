from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import Assets

# Create your views here.
def LoginView(request):
    if request.method == "POST":
        pass
    else:
        return render(request,"inventorymanager/register.html")

class AssetTypeView(generic.ListView) :
    template_name = "inventorymanager/assettype.html"
    context_object_name = "atypes_dict"

    def get_queryset(self) -> QuerySet[Any]:
        out = {}
        for i in Assets.objects.all() :
            if i.category not in out:
                out[i.category] = 0
            out[i.category] += 1
        return out

class AssetsView(generic.ListView):
    template_name = "inventorymanager/assets.html"
    context_object_name = "assets_list"

    def get_queryset(self) -> QuerySet[Any]:
        return Assets.objects.all()

class EmployeesView(generic.ListView) :
    template_name = "inventorymanager/employees.html"
    context_object_name = "employees_tuple"

    def get_queryset(self) -> QuerySet[Any]:
        out = {}
        categories = []
        for i in Assets.objects.all() :
            if i.category not in categories:
                categories.append(i.category)
        for i in Assets.objects.all() :
            if i.employee not in out:
                out[i.employee] = {j:0 for j in sorted(categories)}
            out[i.employee][i.category] += 1
        return (out,sorted(categories))