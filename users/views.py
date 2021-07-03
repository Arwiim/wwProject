from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User
from .utils import generate_token
#


from .models import Profile
from .forms import (UserRegistration, ProfileEditForm, UserEditForm,
                    LoginForm, RecoverPasswordForm, RecoverPasswordFormConfirm)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistration(request.POST)
        if user_form.is_valid():
            #Create user
            new_user = user_form.save(commit=False)
            # Set the chosen passwword
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            user_log = authenticate(username = user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
            #login(request, user_log)
            # Email validator
            send_email_activation(new_user, request)
            messages.add_message(request, messages.SUCCESS, 'We sent email verify')
            return HttpResponseRedirect('/')
    else:
        user_form = UserRegistration()
    return render(request, 'account/register.html', context={'user_form': user_form})


def send_email_activation(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('account/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    send_mail(email_subject,
              email_body,
              'arwiimm@gmail.com',
              [user.email],
              fail_silently=False,)


@login_required
def edit_profile(request):
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
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user and not user.is_verified:
                return HttpResponseRedirect('/')
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
    return []
    # if request.method == 'POST':
    #     form = RecoverPasswordForm(request.POST)
    #     #user = cd['']
    #     #if user is not None:
    #         #if user.is_active():
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         try:
    #             user = User.objects.get(email=cd['email'])
    #             HttpResponse('Email Sended')
    #             send_mail('Recovery Password WW',
    #                   f'Here is your code, {recovery}',
    #                   'arwiimm@gmail.com',
    #                   [cd['email']],
    #                   fail_silently=False)
    #             return HttpResponseRedirect('recover-confirm')
    #         except:
    #             #if not user.is_active():
    #             HttpResponse('No sr')
    #             return HttpResponseRedirect('/')
    #             #print(user)
    # else:
    #     form = RecoverPasswordForm()
    # return render(request, 'account/password_reset.html', {'form_recover': form})    
                   
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

def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('users:login'))

    return render(request, 'account/activate-failed.html', {"user": user})