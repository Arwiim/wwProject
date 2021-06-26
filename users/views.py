from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy



from .models import Profile
from .forms import (UserRegistration, ProfileEditForm, UserEditForm,
                    LoginForm)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistration(request.POST)
        if user_form.is_valid():
            #Create user
            new_user = user_form.save(commit=False)
            # Set the chosen passw
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            user_log = authenticate(username = user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
            login(request, user_log)
            return render(request, 'account/register_done.html', context={'new_user': new_user})
    else:
        user_form = UserRegistration()
    return render(request, 'account/register.html', context={'user_form': user_form})


@login_required
def edit_profile(request):
    #Edit Profile
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                     data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Yes!')
        else:
            messages.error(request, 'Error')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request,
                  'account/edit_profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def user_login(request):
    """
    """
    if request.user.is_authenticated:
        return render(request, 'account/main.html')
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            login(request, user)
            return render(request, 'account/main.html')
    else:
        user_form = LoginForm()
    return render(request, 'account/login.html', {'user_form': user_form})


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'account/logout.html')
    
    
def main(request):
    return render(request, 'base.html')