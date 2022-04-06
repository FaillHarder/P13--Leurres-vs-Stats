from django.http import JsonResponse
from django.shortcuts import render

from app.search import forms
from app.search.utils.search import search_top3


# Create your views here.
def search(request):
    form = forms.SearchForm()
    if request.method == "POST":
        skystate_id = request.POST.get("skystate")
        waterstate_id = request.POST.get("waterstate")
        result = search_top3(skystate_id, waterstate_id)
        print(skystate_id, waterstate_id)
        print(result)
        return JsonResponse({"result": result})
    return render(request, "search/search.html", {"form": form})
