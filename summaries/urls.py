from django.conf.urls import url
from . import views

app_name = 'summaries'

urlpatterns = [
    url(
        r'^verfachbuecher/$',
        views.VerfachBuchListView.as_view(),
        name='verfachbuecher_browse'
    ),
    url(
        r'^verfachbuecher/detail/(?P<pk>[0-9]+)$',
        views.VerfachBuchDetailView.as_view(),
        name='verfachbuch_detail'
    ),
    url(
        r'^verfachbuecher/create/$',
        views.VerfachBuchCreate.as_view(),
        name='verfachbuch_create'
    ),
    url(
        r'^verfachbuecher/edit/(?P<pk>[0-9]+)$',
        views.VerfachBuchUpdate.as_view(),
        name='verfachbuch_edit'
    ),
    url(
        r'^verfachbuecher/delete/(?P<pk>[0-9]+)$',
        views.VerfachBuchDelete.as_view(),
        name='verfachbuch_delete'),
    url(
        r'^inventory/$',
        views.InventoryEntryListView.as_view(),
        name='inventory_browse'
    ),
    url(
        r'^inventory/detail/(?P<pk>[0-9]+)$',
        views.InventoryEntryDetailView.as_view(),
        name='inventory_detail'
    ),
    url(
        r'^inventory/create/$',
        views.InventoryEntryCreate.as_view(),
        name='inventory_create'
    ),
    url(
        r'^inventory/edit/(?P<pk>[0-9]+)$',
        views.InventoryEntryUpdate.as_view(),
        name='inventory_edit'
    ),
    url(
        r'^inventory/delete/(?P<pk>[0-9]+)$',
        views.InventoryEntryDelete.as_view(),
        name='inventory_delete'
    ),
]
