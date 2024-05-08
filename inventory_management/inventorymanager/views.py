from django.shortcuts import render
from django.views import generic

# Create your views here.
def LoginView(request):
    if request.method == "POST":
        pass
    else:
        return render(request,"inventorymanager/register.html")