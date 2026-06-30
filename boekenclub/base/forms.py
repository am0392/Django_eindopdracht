from django import forms
from .models import ReadingSession, Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ReadingSessionForm(forms.ModelForm):
    class Meta:
        model = ReadingSession
        fields = ('book', 'date', 'score')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(approved=True)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("city", "date_of_birth", "favorite_genre")
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"})
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'publication_year', 'genre']
