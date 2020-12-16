from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50)
    #home_address = forms.CharField(max_length=200)
    email = forms.EmailField()
    #date_of_birth = forms.DateField()
    #personal_id = forms.ImageField()

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username',
                  'email','password1', 'password2']