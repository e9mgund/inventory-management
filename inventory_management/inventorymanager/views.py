from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render , redirect
from django.views import generic
from .models import Assets , CustomUser
from .forms import AssetsForm , RegistrationForm
from django.contrib.auth import login , get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

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


class NewEntryView(generic.edit.CreateView):
    model = Assets
    fields = '__all__'

def newFill(request):
    form = AssetsForm

    # if request.method == "GET":
    #     return render(request,"inventorymanager/new_entry.html")

    if request.method == "POST":
        form = AssetsForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context = {"Error":"Error ocurred."}
            return render(request,"inventorymanager/new_entry.html",context)
    context = {"form": form}
    return render(request, "inventorymanager/new_entry.html", context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request,user)
            return redirect('inventorymanager:newbase')
        else:
            return render(request,'inventorymanager/register.html',{'error':form.errors})
    else :
        form = RegistrationForm()
    return render(request,'inventorymanager/register.html',{'form':form})

def Login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user = CustomUser.objects.get(email=email)
    except:
        print(messages.error)
    
    if user is not None:
        return redirect('inventorymanager:newbase')