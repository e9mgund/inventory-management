from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Assets(models.Model) :
    equipment_id = models.CharField(max_length=30)
    equipment_name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    employee = models.CharField(default="Not Assigned",max_length=30)
    assigned_on = models.DateField(default=timezone.now)

    def __str__(self) :
        return self.equipment_id

class CustomUser(models.Model):
    user = models.OneToOneField(User,default="", on_delete=models.CASCADE)
    compname = models.CharField(max_length=100)