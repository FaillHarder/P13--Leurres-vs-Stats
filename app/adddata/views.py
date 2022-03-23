from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms


@login_required
def catchfish(request):
    form = forms.CatchFishForm()
    if request.method == 'POST':
        form = forms.CatchFishForm(request.POST)
        if form.is_valid():
            catch_fish = form.save(commit=False)
            catch_fish.fisherman = request.user
            form.save()
            return redirect('index')
    return render(request, "adddata/catchfish.html", {"form": form})
