"""Module views for users
"""
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from core.posts.models import Post
from .utils import generate_token, temperature
from .models import Profile, User, Favorites
from .forms import UserRegistration, ProfileEditForm, UserEditForm, LoginForm


def main(request):
    """Main view"""
    temp =  temperature()
    return render(request, 'base.html', context={'temp':temp})


def register(request):
    """Register view for user"""
    if request.method == 'POST':
        user_form = UserRegistration(request.POST)
        if user_form.is_valid():
            # Create user
            new_user = user_form.save(commit=False)
            # Set the chosen passwword
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            # Send email for verification
            send_email_activation(new_user, request)
            return render(request, 'account/activate_email.html')
    else:
        user_form = UserRegistration()
    return render(request, 'account/register.html', context={'user_form': user_form})


def send_email_activation(user, request):
    """Function to send email validator after register"""
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string(
        'account/activate.html',
        {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        },
    )
    send_mail(
        email_subject,
        email_body,
        'arwiimm@gmail.com',
        [user.email],
        fail_silently=False,
    )


@login_required
def edit_profile(request):
    """View for porfile edit"""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Yes!')
        else:
            messages.error(request, 'Error')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    post_by_user = Post.objects.filter(user=request.user.id)
    favorites = Favorites.objects.filter(user_from=request.user.id)

    return render(
        request,
        'account/edit_profile.html',
        {'user_form': user_form,
         'profile_form': profile_form,
         'posts': post_by_user,
         'favorites': favorites},
    )


def user_login(request):
    """View for loguin user"""
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            clean_data = user_form.cleaned_data
            user = authenticate(request, username=clean_data['username'], password=clean_data['password'])
            if user:
                if user.is_verified:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return HttpResponseRedirect('/')
                messages.error(request, 'Activate your email')
            else:
                messages.error(request, 'Invalid Credentials')

    user_form = LoginForm()
    return render(request, 'account/login.html', {'user_form': user_form})


@login_required
def user_logout(request):
    """View for user logout"""
    logout(request)
    return HttpResponseRedirect('/')


def activate_user(request, uidb64, token):
    """View for activate a user if the token is the same as the validation"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:  # pylint: disable=global-statement
        user = None

    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Email verified, you can now login')
        return redirect(reverse('users:login'))

    return render(request, 'account/activate-failed.html', {"user": user})


def add_favorite(request, id):
    
    if request.method == 'POST':
        
        userf = request.user
        postf = Post.objects.get(id=id)
        Favorites.objects.create(
            user_from=userf,
            post_fav=postf
        )
        
        return HttpResponseRedirect(
            reverse('posts:lists_posts')
        )