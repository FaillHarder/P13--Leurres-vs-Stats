from django.shortcuts import render

from app.fishingstats.create_stats import FishingStats
from app.fishingstats.utils.generate_stats_choices import AllStatsByChoices


# Create your views here.
def stats(request):
    context = {}
    top_overwall = FishingStats().top_overall_lures_and_colors()
    top_by_choice = AllStatsByChoices().generate_all()

    context["top_overwall"] = top_overwall
    context["top_by_choice"] = top_by_choice

    return render(request, 'fishingstats/stats.html', context)
