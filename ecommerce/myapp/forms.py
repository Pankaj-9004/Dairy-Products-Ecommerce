from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from . models import Customer

class UserRegisterationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))
    

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'state', 'zipcode', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
        
        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus': 'True', 'autocomplete': 'current-password', 'class':'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))
    

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Conform New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))