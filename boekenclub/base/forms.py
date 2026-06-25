from django import forms
from .models import ReadingSession

class ReadingSessionForm(forms.ModelForm):
    class Meta:
        model = ReadingSession
        fields = ('Book', 'Date', 'Score')
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Score': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }