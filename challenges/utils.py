from django.db.models import Sum
from django.db.models.functions import Coalesce


def annotate_score(queryset):
    return (queryset
            .annotate(points=Coalesce(Sum('solved_challenges__points'), 0))
            .order_by('points'))

