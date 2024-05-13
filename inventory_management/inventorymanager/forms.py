from django.forms import ModelForm
from .models import Assets



class AssetsForm(ModelForm):
    class Meta:
        model = Assets
        fields = "__all__"