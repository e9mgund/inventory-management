from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render , redirect , get_object_or_404
from django.views import generic
from .models import Assets , Allocated , Categories
from .forms import AssetsForm , UserRegisterForm
from django.contrib.auth import login , get_user_model, authenticate , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin



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
        Asset_records = list(Assets.objects.all())
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

def addfield(request):
    if request.method == 'POST':
        eq_id = request.POST.get('equipment_id')
        eq_code = request.POST.get('equipment_code')
        eq_name = request.POST.get('equipment_name')
        desc = request.POST.get('description')
        cat = request.POST.get('catgeory')

        categories = Categories.objects.values_list()[0][0]
        print(categories)

        record = Assets(equipment_id=eq_id,equipment_code=eq_code,equipment_name=eq_name,description=desc,category_name_id=categories)
        record.save()
        return redirect('inventorymanager:newbase')

        # if form.is_valid():
        #     form.save()
        #     return JsonResponse({'success':True})
        # else:
        #     return JsonResponse({'errors':form.errors})
    else:
        categories = list(Categories.objects.values())
        eq_id = int(Assets.objects.last().equipment_id) + 1
    return render(request,'inventorymanager/add_new_inventory.html',{'categories':categories,'eq_id':eq_id})

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

class LogoutView(generic.TemplateView):
    def get(self,request):
        logout(request)
        return redirect('inventorymanager:login')