from django.contrib import admin
from .models import *


class WorkAdmin(admin.ModelAdmin):
    list_display = [
        'legacy_id',
        'title',
    ]


class CreatorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'creator_certainty',
        'normdata_id',
    ]


class ExampleAdmin(admin.ModelAdmin):
    list_display = [
        'normdata_id',
    ]


class WorkCreatorAdmin(admin.ModelAdmin):
    list_display = [
        'related_work',
        'related_creator',
    ]


class WorkExampleAdmin(admin.ModelAdmin):
    list_display = [
        'related_work',
        'related_example',
        'certainty'
    ]


admin.site.register(Creator, CreatorAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(WorkCreator, WorkCreatorAdmin)
admin.site.register(Example, ExampleAdmin)
admin.site.register(WorkExample, WorkExampleAdmin)
