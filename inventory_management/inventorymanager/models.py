from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model) :
    category_name = models.CharField(unique=True,max_length=20)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name


class Assets(models.Model) :
    equipment_id = models.CharField(max_length=30)
    equipment_code = models.CharField(default=None,max_length=100,unique=True)
    equipment_name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    category_name = models.ForeignKey(Categories,on_delete=models.CASCADE)
    in_out = models.BooleanField(default=False)

    def __str__(self) :
        return self.equipment_name


class CustomUser(models.Model):
    user = models.OneToOneField(User,default="", on_delete=models.CASCADE)
    compname = models.CharField(max_length=100)


class Transactions(models.Model) :
    equipment_ID = models.ForeignKey(Assets,on_delete=models.CASCADE)
    user = models.CharField(max_length=50,default="Not Assigned")
    T_types = (("IN","IN"),("OUT","OUT"),("EDIT","EDIT"))
    Transaction_type = models.CharField(choices=T_types,max_length=5)
    Transaction_date = models.DateField(default=timezone.now)
    category_name = models.ForeignKey(Categories,on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Allocated(models.Model) :
    equipment_id = models.ForeignKey(Assets,on_delete=models.CASCADE)
    user = models.CharField(max_length=30)
    assigned_on = models.DateField(default=timezone.now)
    category_name = models.ForeignKey(Categories,on_delete=models.CASCADE)

    def __str__(self):
        return self.user