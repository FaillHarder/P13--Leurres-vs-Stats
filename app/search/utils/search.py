from app.adddata.models import SkyState, WaterState
from app.fishingstats.create_stats import ChoicesTop, FishingStats


def search_top3(skystate_id, waterstate_id):
    """Function take id argument

    Args:
        skystate_id (_type_): _description_
        waterstate_id (_type_): _description_

    Returns:
        tuple:
            - top3_list lures
            - top3_list colors

    """
    top3_lure = []
    top3_color = []
    skystate = SkyState.objects.get(pk=skystate_id)
    waterstate = WaterState.objects.get(pk=waterstate_id)

    lures = FishingStats().top_by_states(
        ChoicesTop.LURE,
        skystate.name,
        waterstate.name
    ).filter(num__gt=0)[:3]

    colors = FishingStats().top_by_states(
        ChoicesTop.COLOR,
        skystate.name,
        waterstate.name
    ).filter(num__gt=0)[:3]

    for lure in lures:
        top3_lure.append(lure.name.title())
    for color in colors:
        top3_color.append([color.name.title(), f"{color.image}"])

    return top3_lure, top3_color
