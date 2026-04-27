from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from . models import Contact, Profile


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'message']

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length = 150)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'state', 'pix']

STATE= [
    ('Abuja','Abuja'),
    ('Abia','Abia'),
    ('Edo','Edo'),
    ('Delta','Delta'),
    ('Kogi','kogi')
]