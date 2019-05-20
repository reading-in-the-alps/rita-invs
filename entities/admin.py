from django.contrib import admin
from .models import *
from reversion.admin import VersionAdmin


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


class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'forename',
        'written_name',
    ]


class PersonPersonAdmin(admin.ModelAdmin):
    list_display = [
        'source',
        'rel_type',
        'target',
    ]


admin.site.register(Place, VersionAdmin)
admin.site.register(AlternativeName, VersionAdmin)
admin.site.register(Institution, VersionAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonPerson, PersonPersonAdmin)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(WorkCreator, WorkCreatorAdmin)
admin.site.register(Example, ExampleAdmin)
admin.site.register(WorkExample, WorkExampleAdmin)
