from django.shortcuts import redirect, render

from . import forms


def catchfish(request):
    form = forms.CatchFishForm()
    if request.method == 'POST':
        form = forms.CatchFish(request.POST)
        if form.is_valid():
            return redirect('index')
    return render(request, "adddata/catchfish.html", {"form": form})
