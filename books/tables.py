import django_tables2 as tables
from django_tables2.utils import A

from browsing.browsing_utils import MergeColumn
from . models import *


class WorkTable(tables.Table):
    id = tables.LinkColumn()

    class Meta:
        model = WorkCreator
        sequence = ('id', 'title', 'title_certainty')
        attrs = {"class": "table table-responsive table-hover"}


class WorkCreatorTable(tables.Table):
    id = tables.LinkColumn()
    related_work = tables.LinkColumn(
        'books:work_detail',
        args=[A('related_work.id')], verbose_name='Work'
    )
    related_creator = tables.LinkColumn(
        'books:creator_detail',
        args=[A('related_creator.id')], verbose_name='creator'
    )
    certainty = tables.Column()

    class Meta:
        model = WorkCreator
        sequence = ('id', 'related_work', 'related_creator', 'certainty')
        attrs = {"class": "table table-responsive table-hover"}
