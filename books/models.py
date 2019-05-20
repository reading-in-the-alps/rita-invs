from django.db import models
from django.urls import reverse
from vocabs.models import SkosConcept

from idprovider.models import IdProvider


class Creator(IdProvider):
    """Beschreibt einen Akteur der für die Erzeugung eines Werkes verantwortlich war."""
    legacy_id = models.CharField(
        max_length=250, blank=True,
        verbose_name="Lokale ID",
        help_text="Lokaler Identifier (rita.acdh.oeaw.ac.at)"
    )
    name = models.CharField(
        max_length=250, blank=True,
        verbose_name="Name",
        help_text="Normalisierte Namensansetzung"
    )
    normdata_id = models.CharField(
        max_length=350, blank=True,
        verbose_name="Normdaten ID",
        help_text="Link zu Normdateneintrag"
    )
    creator_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Gewissheit (Titel)",
        help_text="Wie sicher ist es, dass genau dieser Erzeuger gemeint war",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "{}".format(self.name)


class Work(IdProvider):
    legacy_id = models.CharField(
        max_length=250, blank=True,
        verbose_name="Lokale ID",
        help_text="Lokaler Identifier (rita.acdh.oeaw.ac.at)"
    )
    title = models.CharField(
        max_length=450, blank=True,
        verbose_name="Titel",
        help_text="(Normalisierter) Titel des Werkes"
    )
    year_of_origin = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Erscheinungsjahr",
        help_text="Jahr der Erstveröffentlichung"
    )
    title_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Gewissheit (Titel)",
        help_text="Wie sicher ist die Titelansetzung",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "{}".format(self.title)

    @classmethod
    def get_listview_url(self):
        return reverse('books:work_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('books:work_create')

    def get_absolute_url(self):
        return reverse('books:work_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('books:work_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('books:work_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('books:work_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'books:work_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'books:work_detail',
                kwargs={'pk': prev.first().id}
            )
        return False


class Example(IdProvider):
    title = models.CharField(
        max_length=250, blank=True,
        verbose_name="Titel",
        help_text="(Normalisierter) Titel des Werkes"
    )
    normdata_id = models.CharField(
        max_length=350, blank=True,
        verbose_name="Normdaten ID",
        help_text="Link zu Normdateneintrag"
    )

    def __str__(self):
        if self.title:
            return "{}".format(self.title)
        elif self.normdata_id:
            return "{}".format(self.normdata_id)
        else:
            return "{}".format(self.id)


class WorkExample(IdProvider):
    related_work = models.ForeignKey(
        Work, blank=True, null=True,
        verbose_name="Werk",
        on_delete=models.SET_NULL
    )
    related_example = models.ForeignKey(
        Example, blank=True, null=True,
        verbose_name="Exemplar",
        help_text="Exemplar",
        on_delete=models.SET_NULL
    )
    certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Gewissheit",
        help_text="Wie sicher ist diese Verbindung",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "{} {}".format(self.related_work, self.related_example)


class WorkCreator(IdProvider):
    related_work = models.ForeignKey(
        Work, blank=True, null=True,
        verbose_name="Werk",
        on_delete=models.SET_NULL
    )
    related_creator = models.ForeignKey(
        Creator, blank=True, null=True,
        verbose_name="Erzeuger",
        help_text="Verantwortlich für die Erzeugung des Werkes",
        on_delete=models.SET_NULL
    )
    certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Gewissheit",
        help_text="Wie sicher ist diese Verbindung",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "{} {}".format(self.related_work, self.related_creator)


# Create your models here.
