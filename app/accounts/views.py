from .froms import CreateProfilForm
from .models import Profile
from app.adddata.forms import CatchFishForm
from app.adddata.models import CatchFish

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404


@login_required
def profile(request):
    user = request.user
    context = {}
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        mail = user.email
        pseudo = mail[:mail.find('@')]
        profile = Profile.objects.create(user=user, pseudo=pseudo)

    catch_list = CatchFish.objects.filter(fisherman=user.pk)
    catch_list_count = catch_list.count()
    context["user_profile"] = profile
    context["count"] = catch_list_count
    return render(request, "accounts/profile.html", context=context)


@login_required
def edit_profile(request):
    user = request.user.profile
    form = CreateProfilForm(instance=user)
    if request.method == "POST":
        form = CreateProfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def my_catch(request):
    user = request.user
    catch_list = CatchFish.objects.filter(fisherman=user.pk).order_by("-pk")
    paginator = Paginator(catch_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "accounts/my_catch.html", {'page_obj': page_obj})


@login_required
def my_catch_edit(request, id):
    catch = get_object_or_404(CatchFish, pk=id)
    form = CatchFishForm(instance=catch)
    if request.method == "POST":
        form = CatchFishForm(request.POST, instance=catch)
        if form.is_valid():
            form.save()
            return redirect("my_catch")
    return render(request, "accounts/my_catch_edit.html", {"catch": catch, "form": form})


@login_required
def my_catch_delete(request, id):
    catch = get_object_or_404(CatchFish, pk=id)
    if request.method == "POST":
        catch.delete()
        return redirect("my_catch")
    return render(request, "accounts/my_catch_delete.html", {"catch": catch})
