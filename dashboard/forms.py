from django import forms
from .models import CarpoolPost

class CarpoolPostForm(forms.ModelForm):
    class Meta:
        model = CarpoolPost
        fields = ['text', 'image', 'image_visibility']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your carpool trip...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_visibility': forms.Select(attrs={'class': 'form-control'}),
        }