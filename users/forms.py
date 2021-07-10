from django import db, forms
from django.core.exceptions import ValidationError
from .models import Profile, User

def email_validation(email):
    if not email:
        ValidationError('Put email!')
    ValidationError('Jesus')
class UserRegistration(forms.Form):
    """Form for user registration
    """
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)
    username = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)
    email = forms.EmailField(required=True,
                             max_length=70,
                             label='Email',
                             validators=[email_validation,])
        
    def clean_password2(self):
        super(UserRegistration, self).clean()
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password not match')
        return cd['password2']
    
    def clean_email(self):
        super(UserRegistration, self).clean()
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('This email address is already taken!')
            else:
                pass
        return email

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
                               widget=forms.PasswordInput)
