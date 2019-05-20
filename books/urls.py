from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns = [
    url(
        r'^work/$',
        views.WorkListView.as_view(),
        name='work_browse'
    ),
    url(
        r'^work/detail/(?P<pk>[0-9]+)$',
        views.WorkDetailView.as_view(),
        name='work_detail'
    ),
    url(
        r'^work/create/$',
        views.WorkCreate.as_view(),
        name='work_create'
    ),
    url(
        r'^work/edit/(?P<pk>[0-9]+)$',
        views.WorkUpdate.as_view(),
        name='work_edit'
    ),
    url(
        r'^work/delete/(?P<pk>[0-9]+)$',
        views.WorkDelete.as_view(),
        name='work_delete'),
]
