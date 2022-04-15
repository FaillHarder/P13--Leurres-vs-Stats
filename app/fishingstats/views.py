from django.shortcuts import render

from app.fishingstats.create_stats import ChoicesTop, FishingStats
from app.fishingstats.utils.generate_stats_choices import AllStatsByChoices


# Create your views here.
def stats(request):
    context = {}

    top_overwall_lure = FishingStats().top_overall(ChoicesTop.LURE)
    top_overwall_color = FishingStats().top_overall(ChoicesTop.COLOR)
    top_lure_color_by_states = AllStatsByChoices().generate_all()

    context["top_overwall_lure"] = top_overwall_lure
    context["top_overwall_color"] = top_overwall_color
    context["top_lure_color_by_states"] = top_lure_color_by_states

    return render(request, 'fishingstats/stats.html', context)
