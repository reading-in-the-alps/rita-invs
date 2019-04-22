import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from entities.models import Person


class Command(BaseCommand):
    # Show this when the user types help
    help = "populates the written_name_leven field with the first 254 chars written_name field"

    # A command must define handle()
    def handle(self, *args, **options):

        self.stdout.write("start")
        for x in Person.objects.all():
            x.written_name_leven = x.written_name[:254]
            x.save()

        self.stdout.write("finished")
