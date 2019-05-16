import django_filters

from dal import autocomplete
from django import forms

from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from entities.models import Institution
from . models import *


class InventoryEntryListFilter(django_filters.FilterSet):
    inv_signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=InventoryEntry._meta.get_field('inv_signatur').help_text,
        label=InventoryEntry._meta.get_field('inv_signatur').verbose_name
    )
    is_located_in__signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=InventoryEntry._meta.get_field('is_located_in').help_text,
        label=InventoryEntry._meta.get_field('is_located_in').verbose_name
    )
    excel_row = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=InventoryEntry._meta.get_field('excel_row').help_text,
        label=InventoryEntry._meta.get_field('excel_row').verbose_name
    )

    class Meta:
        model = InventoryEntry
        fields = "__all__"


class VerfachBuchListFilter(django_filters.FilterSet):
    signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=VerfachBuch._meta.get_field('signatur').help_text,
        label=VerfachBuch._meta.get_field('signatur').verbose_name
    )
    year = django_filters.DateFromToRangeFilter(
        help_text=VerfachBuch._meta.get_field('year').help_text,
        label=VerfachBuch._meta.get_field('year').verbose_name
    )
