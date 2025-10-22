from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DriverProfile, RiderProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['name', 'computing_id', 'phone_number', 'gender', 'class_year', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'computing_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'class_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class RiderProfileForm(forms.ModelForm):
    class Meta:
        model = RiderProfile
        fields = ['name', 'computing_id', 'phone_number', 'gender', 'class_year', 'profile_picture', 'ride_preference']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'computing_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'class_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'ride_preference': forms.TextInput(attrs={'class': 'form-control'}),
        }