from django.db import models

# Create your models here.

class AssetType(models.Model) :
    type_name = models.CharField(max_length=20)
    type_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.type_name

class Assets(models.Model) :
    equipment_id = models.CharField(max_length=30)
    equipment_name = models.CharField(max_length=30)
    category = models.ForeignKey(
        AssetType , on_delete=models.CASCADE
    )

    def __str__(self) :
        return self.equipment_name