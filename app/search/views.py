from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from app.search import forms
from app.search.utils.search import search_top3


@login_required
def search(request):
    form = forms.SearchForm()
    if request.method == "POST":
        skystate_id = request.POST.get("skystate")
        waterstate_id = request.POST.get("waterstate")
        result = search_top3(skystate_id, waterstate_id)
        return JsonResponse({"lures": result[0], "colors": result[1]})
    return render(request, "search/search.html", {"form": form})
