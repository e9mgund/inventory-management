from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Assets)
admin.site.register(Categories)
admin.site.register(Transactions)
admin.site.register(Allocated)