from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm
from .models import Profile,Contact
from django.contrib import admin

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'contact_number', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact no.'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write your message', 'rows': 4})
        }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is not registered.")
        return email


class RegistrationForm(UserCreationForm):  
    class Meta:
        model=User
        fields = ["username", "email", "password1"]
        
class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget =forms.PasswordInput)

# event/forms.py

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    class Meta:
        model = forms.Form
        fields = ['email']


class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")

class AdminForm(forms.Form):
        adminname = forms.CharField()
        password = forms.CharField(widget =forms.PasswordInput)

 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','mobile', 'alternate', 'address', 'city', 'state', 'zipcode']

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name', 'email', 'contact_number', 'message']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Your name'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email'
#             }),
#             'contact_number': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Contact no.'
#             }),
#             'message': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Write your message',
#                 'rows': 7
#             }),
#         }