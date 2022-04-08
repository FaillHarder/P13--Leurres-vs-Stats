from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from . import forms


def create_user(request):
    form = forms.CreateUserForm()
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "usermanager/registrer.html", {"form": form})


def login_user(request):
    message = ""
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get(
                        'next',
                        settings.LOGIN_REDIRECT_URL
                    )
                )
            else:
                message = "Email ou mot de passe invalide."
                form = forms.LoginForm()
    return render(request, 'usermanager/registration/login.html', context={"form": form, "message": message})


def logout_user(request):
    logout(request)
    return redirect('index')
