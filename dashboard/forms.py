from django import forms
from .models import CarpoolPost
from datetime import date

class CarpoolPostForm(forms.ModelForm):
    class Meta:
        model = CarpoolPost
        fields = ['name', 'date', 'pickup_time', 'dropoff_time', 'dropoff', 'pickup', 'notes', 'image', 'image_visibility']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'rows':1, 'placeholder': 'Name of Carpool Trip', 'required': True}),
            'date': forms.DateInput(attrs={'class':'form-control', 'type': 'date', 'required': True}),
            'pickup_time': forms.TimeInput(attrs={'class':'form-control', 'type': 'time', 'required': True}),
            'dropoff_time': forms.TimeInput(attrs={'class':'form-control', 'type': 'time', 'required': True}),
            'dropoff': forms.TextInput(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Street, City, State, Zip Code', 'required': True}),
            'pickup': forms.TextInput(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Street, City, State, Zip Code', 'required': True}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe additional details about your carpool trip...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_visibility': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = date.today().isoformat()
    
    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < date.today():
            raise forms.ValidationError("Trip date cannot be in the past.")
        return selected_date