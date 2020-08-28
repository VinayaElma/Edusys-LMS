from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Department, Subject


class DateInput(forms.DateInput):
    input_type= 'date'

class RegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=DateInput)
    class Meta:
        model = User
        fields = ['username', 'first_name' , 'last_name' ,
            'profile_pic' , 'email' , 'password1' , 'password2',
            'phone_number', 'date_of_birth', 'department' ,
            'user_type' , 'position' , 'roll_number',
            'semester', 'year_of_admission']


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
             'first_name' , 'last_name' ,
            'profile_pic' , 'email' ,
            'phone_number', 'date_of_birth', 'department' ,
            'user_type' , 'position' , 'roll_number',
            'semester', 'year_of_admission' , 'subjects'
        ]
        




               