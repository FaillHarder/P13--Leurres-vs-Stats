from django.db.models import Count, Q

from app.adddata.models import Lure, Color


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
    lures = Lure.objects.annotate(
            num=Count(
                "catchfish",
                filter=Q(catchfish__sky_state__id=skystate_id)
                & Q(catchfish__water_state__id=waterstate_id)
                )
            ).order_by("-num").filter(num__gt=0)[:3]

    colors = Color.objects.annotate(
            num=Count(
                "catchfish",
                filter=Q(catchfish__sky_state__id=skystate_id)
                & Q(catchfish__water_state__id=waterstate_id)
                )
            ).order_by("-num").filter(num__gt=0)[:3]

    for lure in lures:
        top3_lure.append(lure.name)
    for color in colors:
        top3_color.append([color.name, f"{color.image}"])

    return top3_lure, top3_color
