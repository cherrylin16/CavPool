from django import forms
from .models import CarpoolPost

class CarpoolPostForm(forms.ModelForm):
    class Meta:
        model = CarpoolPost
        fields = ['name', 'date', 'pickup_time', 'dropoff_time', 'dropoff', 'pickup', 'notes', 'image', 'image_visibility']
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'placeholder': 'Name of Carpool Trip'}),
            'date': forms.Textarea(attrs={'class':'form-control', 'rows': 1, 'placeholder': 'Ex: Thursday, September 22'}),
            'pickup_time': forms.Textarea(attrs={'class':'form-control', 'rows': 1, 'placeholder': 'Ex: 10:00 AM'}),
            'dropoff_time': forms.Textarea(attrs={'class':'form-control', 'rows': 1, 'placeholder': 'Ex: 5:00 PM'}),
            'dropoff': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Street, City, State, Zip Code'}),
            'pickup': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Street, City, State, Zip Code'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe additional details about your carpool trip...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_visibility': forms.Select(attrs={'class': 'form-control'}),
        }