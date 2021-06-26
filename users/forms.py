from django import forms
from django.forms import models
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from .models import Profile

class UserRegistration(forms.ModelForm):
    """Form for user registration
    """
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password not match')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    #
    class Meta:
        model = Profile
        fields = ('website','photo', 'date_of_birth')


class LoginForm(forms.Form):
    """
    """
    username = forms.CharField(label='Email or User')
    password = forms.CharField(label='Password',
                               widget=PasswordInput)
    # class Meta:
    #     model = User
    #     fields = ('password',)