from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render , redirect , get_object_or_404
from django.views import generic
from .models import Assets , Allocated , Categories , Transactions
from .forms import AssetsForm , UserRegisterForm
from django.contrib.auth import login , get_user_model, authenticate , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from json import dumps
from django.utils import timezone
from datetime import datetime



# Create your views here.


class RecordsView(generic.ListView):
    template_name = "inventorymanager/newbase.html"
    context_object_name = "records"

    def get_queryset(self) -> QuerySet[Any]:
        return Assets.objects.all()

class HomeView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'inventorymanager/newbase.html'
    redirect_field_name = None
    login_url = 'inventorymanager:login'
    
    def get_context_data(self, **kwargs: Any) :
        Asset_records = [i for i in list(Assets.objects.all()) if not i.in_out]
        Allocated_records = list(Allocated.objects.values())
        return {'Asset_records':Asset_records,'Asset_count':len(Asset_records),'Allocated_records':len(Allocated_records)}
    
    def addfield(self,request):
        if request.method == 'POST':
            form = AssetsForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'success':True})
            else:
                return JsonResponse({'errors':form.errors})
        else:
            form = AssetsForm()
        return render(request,'inventorymanager/add_new_inventory.html',{'add_form':form})

class AllocatedView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'inventorymanager/allocated.html'
    redirect_field_name = None
    login_url = 'inventorymanager:login'

    def get_context_data(self, **kwargs: Any):
        Asset_records = [i for i in list(Assets.objects.all()) if not i.in_out]
        Allocated_records = Allocated.objects.all()
        return {'Allocated_records':Allocated_records,'Asset_count':len(Asset_records),'Allocated_count':len(list(Allocated_records))}


def addfieldAllocated(request):
    if request.method == 'POST':
        if request.POST.get("Transaction_type") == "OUT":
            equipment_id = request.POST.get('equipment_id')
            user = request.POST.get('user')
            Transaction_type = request.POST.get('Transaction_type')
            Transaction_date = request.POST.get('Transaction_date')
            category_id = request.POST.get('category_name_id')
            transaction_record = Transactions(equipment_ID_id=equipment_id,user=user,Transaction_type=Transaction_type,Transaction_date=Transaction_date,category_name_id=category_id)
            transaction_record.save()
            alloacted_record = Allocated(equipment_id_id=equipment_id,user=user,assigned_on=Transaction_date,category_name_id=category_id)
            alloacted_record.save()
            asset_record = Assets.objects.get(id=equipment_id)
            asset_record.in_out = True
            asset_record.save()
        else:
            pass
    else:
        pass
    categories = [i for i in Categories.objects.values()]
    assets = [i for i in Assets.objects.values() if not i['in_out']]
    return render(request,'inventorymanager/add_new_allocated.html',{'categories':categories,'assets':dumps(assets)})

def addfield(request):
    if request.method == 'POST':
        eq_id = request.POST.get('equipment_id')
        eq_code = request.POST.get('equipment_code')
        eq_name = request.POST.get('equipment_name')
        desc = request.POST.get('description')
        cat = request.POST.get('category_name').strip().lower()
        category_id = None
        for i in Categories.objects.values_list() :
            if cat in i:
                cat_record = Categories.objects.get(category_name=cat)
                cat_record.quantity += 1
                category_id = i[0]
                break
        else:
            cat_record = Categories(category_name=cat,quantity=1)
        cat_record.save()
        category_id = Categories.objects.last().id
        record = Assets(equipment_id=eq_id,equipment_code=eq_code,equipment_name=eq_name,description=desc,category_name_id=category_id,in_out=False)
        record.save()
        transaction_record = Transactions(equipment_ID_id=record.id,user="Not Assigned",Transaction_type="IN",Transaction_date=datetime.now().date(),category_name_id=category_id)
        print(transaction_record.__dict__)
        transaction_record.save()
        return redirect('inventorymanager:newbase')

        # if form.is_valid():
        #     form.save()
        #     return JsonResponse({'success':True})
        # else:
        #     return JsonResponse({'errors':form.errors})
    else:
        categories = list(Categories.objects.values())
    return render(request,'inventorymanager/add_new_inventory.html',{'categories':categories})

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


class LoginView(generic.TemplateView) :
    template_name = 'inventorymanager/login.html'
    def post(self,request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                form = login(request,user)
                return redirect('inventorymanager:newbase')
            else:
                messages.info(request,'account Does not exist')
        form = AuthenticationForm()
        return render(request,self.template_name,{'form':form})

def editfield(request, pk):
    record = get_object_or_404(Assets,pk=pk)
    if request.method == 'POST':
        eq_id = request.POST.get('equipment_id')
        eq_code = request.POST.get('equipment_code')
        eq_name = request.POST.get('equipment_name')
        desc = request.POST.get('description')
        cat = request.POST.get('category_name').strip().lower()
        for i in Categories.objects.values():
            if cat == i['category_name']:
                category_id = i['id']
                break
        else:
            cat_record = Categories(category_name=cat,quantity=1)
            cat_record.save()
            cat_record = Categories.objects.get(category_name=record.category_name)
            if cat_record.quantity < 2 :
                cat_record.delete()
            else:
                cat_record.quantity -= 1
                cat_record.save()
            category_id = Categories.objects.last().id
        if record.equipment_id != eq_id:
            record.equipment_id = eq_id
        elif record.equipment_code != eq_code:
            record.equipment_code = eq_code
        elif record.equipment_name != eq_name:
            record.equipment_name = eq_name
        elif record.description != desc:
            record.description = desc
        record.category_name = Categories.objects.get(id=category_id)
        record.save()


        return redirect('inventorymanager:newbase')
        # form = AssetsForm(request.POST,instance=record)
        # if form.is_valid():
        #     form.save()
        #     return JsonResponse({'success':True})
        # else:
        #     return JsonResponse({'success':False,'error':form.errors},status=400)
    else:
        form = AssetsForm(instance=Assets)
    return render(request,'inventorymanager/editblock.html',{'record':record})

def deletefield(request, pk):
    record = get_object_or_404(Assets,pk=pk)
    if request.method == 'POST':
        record.delete()
        cat_record = Categories.objects.get(category_name=record.category_name)
        if cat_record.quantity < 2 :
            cat_record.delete()
        else:
            cat_record.quantity -= 1
            cat_record.save()
        return JsonResponse({'success':True})
    return render(request,'inventorymanager/deleteblock.html',{'record':record})

def deleteallocated(request, pk):
    record = get_object_or_404(Allocated,pk=pk)
    if request.method == 'POST':
        print(record.__dict__)
        

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

def getallocatedfield(request,record_id):
    record = get_object_or_404(Allocated, id=record_id)

    data = {
        'id':record.id,
        'equipment_id':record.equipment_id,
        'user':record.user,
        'assigned_on':record.assigned_on,
        'category_name':record.category_name
    }
    return JsonResponse(data)

class LogoutView(generic.TemplateView):
    def get(self,request):
        logout(request)
        return redirect('inventorymanager:login')