from . import forms

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render


def create_user(request):
    form = forms.CreateUserForm()
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "usermanager/registrer.html", {"form": form})
