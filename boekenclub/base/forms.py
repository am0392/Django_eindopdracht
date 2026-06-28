from django import forms
from .models import ReadingSession, Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ReadingSessionForm(forms.ModelForm):
    class Meta:
        model = ReadingSession
        fields = ('Book', 'Date', 'Score')
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Score': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Book'].queryset = Book.objects.filter(Approved=True)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("City", "DateOfBirth", "FavoriteGenre")
        widgets = {
            "DateOfBirth": forms.DateInput(attrs={"type": "date"})
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['Name', 'PublicationYear', 'Genre']
