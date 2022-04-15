from django.db.models import Count, Q

from enum import Enum, auto

from app.adddata.models import CatchFish, Lure, Color


class ChoicesTop(Enum):
    COLOR = auto()
    LURE = auto()


class FishingStats():

    def top_by_states(self, choices_top: ChoicesTop, skystate: str, waterstate: str):
        """Method allowing to have the percentage of effectiveness of the lures or
        colors by state of the sky and the water compared to the Catchfish model

        Args:
            choices_top (ChoicesTop): COLOR or LURE
            skystate (str): models.SkyState obj.name
            waterstate (str): models.WaterState obj.name

        Returns:
            queryset with ChoicesTop.LURE parameter:
                - obj.name, obj.num
            queryset with ChoicesTop.COLOR parameter:
                - obj.name, obj.image, obj.num
        """
        if choices_top == ChoicesTop.LURE:
            query_lures = Lure.objects.annotate(
                num=Count(
                    "catchfish",
                    filter=Q(catchfish__sky_state__name=skystate)
                    & Q(catchfish__water_state__name=waterstate)
                    )
                ).order_by("-num")
            return self.convert_to_percentage(query_lures, skystate, waterstate)

        else:
            query_colors = Color.objects.annotate(
                num=Count(
                    "catchfish",
                    filter=Q(catchfish__sky_state__name=skystate)
                    & Q(catchfish__water_state__name=waterstate)
                    )
                ).order_by("-num")
        return self.convert_to_percentage(query_colors, skystate, waterstate)

    def top_overall(self, choices_top: ChoicesTop):
        """Method allowing to have the global percentage of effectiveness
        of the lures or colors compared to the Catchfish model

        Args:
            choices_top (ChoicesTop): COLOR or LURE

        Returns:
            queryset with ChoicesTop.LURE parameter:
                - obj.name, obj.num
            queryset with ChoicesTop.COLOR parameter:
                - obj.name, obj.image, obj.num
        """
        if choices_top == ChoicesTop.LURE:
            query_lures = Lure.objects.annotate(num=Count("catchfish")).order_by("-num")
            return self.convert_to_percentage(query_lures)
        else:
            query_colors = Color.objects.annotate(num=Count("catchfish")).order_by("-num")
            return self.convert_to_percentage(query_colors)

    @staticmethod
    def convert_to_percentage(query_set, sky_state=None, water_state=None):
        """Method to convert queryset num value to percentage

        Args:
            query_set (queryset): return from :
                - top_lure_by_states
                - top_color_by_states
                - top_overall_lure_and_color

        Returns:
            queryset:
                - query.num = num percentage
        """
        catchfish = CatchFish.objects.all()
        if sky_state and water_state:
            catchfish_len = len(
                    catchfish.filter(sky_state__name=sky_state, water_state__name=water_state)
                )
        else:
            catchfish_len = len(catchfish)

        if catchfish_len > 0:
            for obj in query_set:
                obj.num = round(obj.num * 100 / catchfish_len, 2)
            return query_set
        else:
            return query_set
