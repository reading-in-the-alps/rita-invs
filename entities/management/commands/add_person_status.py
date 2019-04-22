import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from entities.models import Person


class Command(BaseCommand):
    # Show this when the user types help
    help = "Updates the status of a Person Inventory relation (main, adm, related, other)"

    # A command must define handle()
    def handle(self, *args, **options):

        self.stdout.write("updating status for main person")
        for x in Person.objects.filter(is_main_person__isnull=False):
            x.is_main = True
            x.save()

        self.stdout.write("updating status for adm person")
        for x in Person.objects.filter(is_adm_person__isnull=False):
            x.is_adm = True
            x.save()

        self.stdout.write("updating status for related person")
        for x in Person.objects.filter(is_related_person__isnull=False):
            x.is_related = True
            x.save()

        self.stdout.write("updating status for other person")
        for x in Person.objects.filter(is_other_person__isnull=False):
            x.is_other = True
            x.save()

        self.stdout.write("everything is up to date")
