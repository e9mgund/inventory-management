from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render , redirect , get_object_or_404
from django.views import generic
from .models import Assets
from .forms import AssetsForm , UserRegisterForm
from django.contrib.auth import login , get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.

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


class RecordsView(generic.ListView):
    template_name = "inventorymanager/newbase.html"
    context_object_name = "records"

    def get_queryset(self) -> QuerySet[Any]:
        return Assets.objects.all()

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

def addfield(request):
    if request.method == 'POST':
        form = AssetsForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'errors':form.errors})
    else:
        form = AssetsForm()
    return render(request,'inventorymanager/addblock.html',{'add_form':form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request,user)
            return redirect('inventorymanager:newbase')
        else:
            return render(request,'inventorymanager/register.html',{'error':form.errors})
    else :
        form = UserRegisterForm()
    return render(request,'inventorymanager/register.html',{'form':form})

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            form = login(request,user)
            messages.success(request,'Welcome')
            return redirect('inventorymanager:overview')
        else:
            messages.info(request,'account Does not exist')
    form = AuthenticationForm()
    return render(request,'inventorymanager/login.html',{'form':form})

def editfield(request, pk):
    record = get_object_or_404(Assets,pk=pk)
    if request.method == 'POST':
        form = AssetsForm(request.POST,instance=record)
        if form.is_valid():
            form.save()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False,'error':form.errors},status=400)
    else:
        form = AssetsForm(instance=Assets)
    return render(request,'inventorymanager/editblock.html',{'form':form,'record':record})

def deletefield(request, pk):
    record = get_object_or_404(Assets,pk=pk)
    if request.method == 'POST':
        record.delete()
        return JsonResponse({'success':True})
    return render(request,'inventorymanager/deleteblock.html',{'record':record})

def getfield(request, record_id):
    record = get_object_or_404(Assets, id=record_id)
    data = {
        'id': record.id,
        'equipment_id': record.equipment_id,
        'equipment_name': record.equipment_name,
        'equipment_code': record.equipment_code,
        'description': record.description,
        'category_name': record.category_name.category_name
    }
    return JsonResponse(data)