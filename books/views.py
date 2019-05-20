from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from . filters import *
from . forms import *
from . tables import *
from . models import *


class WorkListView(GenericListView):
    model = Work
    filter_class = WorkListFilter
    formhelper_class = WorkFilterFormHelper
    table_class = None
    init_columns = [
        'id',
        'title',
    ]
    enable_merge = True


class WorkDetailView(DetailView):
    model = Work
    template_name = 'entities/work_detail.html'


class WorkCreate(BaseCreateView):

    model = Work
    form_class = WorkForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkCreate, self).dispatch(*args, **kwargs)


class WorkUpdate(BaseUpdateView):

    model = Work
    form_class = WorkForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkUpdate, self).dispatch(*args, **kwargs)


class WorkDelete(DeleteView):
    model = Work
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('books:work_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkDelete, self).dispatch(*args, **kwargs)
