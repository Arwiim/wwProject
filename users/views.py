from django import http
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
#
from .decorators import password_code



from .models import Profile
from .forms import (UserRegistration, ProfileEditForm, UserEditForm,
                    LoginForm, RecoverPasswordForm, RecoverPasswordFormConfirm)


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
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        user_form = LoginForm()
    return render(request, 'account/login.html', {'user_form': user_form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_recovery_password(request):
    active = False
    if request.method == 'POST':
        form = RecoverPasswordForm(request.POST)
        #user = cd['']
        #if user is not None:
            #if user.is_active():
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(email=cd['email'])
                recovery = password_code()
                HttpResponse('Email Sended')
                send_mail('Recovery Password WW',
                      f'Here is your code, {recovery}',
                      'arwiimm@gmail.com',
                      [cd['email']],
                      fail_silently=False)
                return HttpResponseRedirect('recover-confirm')
            except:
                #if not user.is_active():
                HttpResponse('No sr')
                return HttpResponseRedirect('/')
                #print(user)
    else:
        form = RecoverPasswordForm()
    return render(request, 'account/password_reset.html', {'form_recover': form})    
                   
def user_password_confirm(request):
    if request.method == 'POST':
        form = RecoverPasswordFormConfirm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(email=cd['email'])
            if user.profile.coderegistro == cd['recovery']:
                return HttpResponseRedirect('/')
    else:
        form = RecoverPasswordFormConfirm()
    return render(request, 'account/password_confirm.html', {'form': form})
    
def main(request):
    return render(request, 'base.html')