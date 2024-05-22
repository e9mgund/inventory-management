from django import forms
from .models import Assets , CustomUser
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User



class AssetsForm(forms.ModelForm):
    class Meta:
        model = Assets
        fields = "__all__"


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','compname']