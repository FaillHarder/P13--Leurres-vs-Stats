from .froms import CreateProfilForm
from .models import Profile
from app.adddata.models import CatchFish

from django.shortcuts import redirect, render


def profile(request):
    context = {}
    user = request.user
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


def edit_profile(request):
    user = request.user.profile
    form = CreateProfilForm(instance=user)
    if request.method == "POST":
        form = CreateProfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, "accounts/edit_profile.html", {"form": form})
