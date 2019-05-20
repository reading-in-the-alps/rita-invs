import django_filters
from dal import autocomplete

from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from . models import *


class WorkListFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Work._meta.get_field('title').help_text,
        label=Work._meta.get_field('title').verbose_name
        )
    title_certainty = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.all(),
        help_text=Work._meta.get_field('title_certainty').help_text,
        label=Work._meta.get_field('title_certainty').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/concept-by-colleciton-ac/certainty",
            )
        )

    class Meta:
        model = Work
        fields = "__all__"


class CreatorListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Creator._meta.get_field('name').help_text,
        label=Creator._meta.get_field('name').verbose_name
        )
    legacy_id = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Creator._meta.get_field('legacy_id').help_text,
        label=Creator._meta.get_field('legacy_id').verbose_name
        )
    normdata_id = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Creator._meta.get_field('normdata_id').help_text,
        label=Creator._meta.get_field('normdata_id').verbose_name
        )
    creator_certainty = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.all(),
        help_text=Creator._meta.get_field('creator_certainty').help_text,
        label=Creator._meta.get_field('creator_certainty').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/concept-by-colleciton-ac/certainty",
            )
        )

    class Meta:
        model = Creator
        fields = "__all__"
