import re
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from idprovider.models import IdProvider
import reversion

from browsing.browsing_utils import model_to_dict
from vocabs.models import SkosConcept

from . utils import get_coordinates


@reversion.register()
class AlternativeName(IdProvider):
    name = models.CharField(
        max_length=250, blank=True, help_text="Alternative Name"
    )

    def get_next(self):
        next = AlternativeName.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = AlternativeName.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return "{}".format(self.name)


@reversion.register()
class Place(IdProvider):
    PLACE_TYPES = (
        ("city", "city"),
        ("country", "country")
    )

    """Holds information about entities."""
    name = models.CharField(
        max_length=250, blank=True, help_text="Normalized name"
    )
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250, blank=True,
        help_text="Alternative names",
        related_name="altname_of_place"
    )
    geonames_id = models.CharField(
        max_length=50, blank=True,
        help_text="GND-ID"
    )
    lat = models.DecimalField(
        max_digits=20, decimal_places=12,
        blank=True, null=True
    )
    lng = models.DecimalField(
        max_digits=20, decimal_places=12, blank=True, null=True
    )
    part_of = models.ForeignKey(
        "Place", null=True, blank=True,
        help_text="A place (country) this place is part of.",
        related_name="has_child",
        on_delete=models.SET_NULL
    )
    place_type = models.CharField(
        choices=PLACE_TYPES, null=True, blank=True, max_length=50
    )

    def get_geonames_url(self):
        if self.geonames_id.startswith('ht') and self.geonames_id.endswith('.html'):
            return self.geonames_id
        else:
            return "http://www.geonames.org/{}".format(self.geonames_id)

    def get_geonames_rdf(self):
        try:
            number = re.findall(r'\d+', str(self.geonames_id))[0]
            return number
        except Exception as e:
            return None

    def save(self, *args, **kwargs):
        if self.geonames_id:
            new_id = self.get_geonames_url()
            self.geonames_id = new_id
        if self.get_geonames_rdf() and not self.lat:
            coords = get_coordinates(self.get_geonames_rdf())
            if coords:
                self.lat = coords['lat']
                self.lng = coords['lng']
        super(Place, self).save(*args, **kwargs)

    @classmethod
    def get_listview_url(self):
        return reverse('entities:place_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:place_create')

    def get_absolute_url(self):
        return reverse('entities:place_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:place_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:place_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'entities:place_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:place_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def __str__(self):
        return "{}".format(self.name)


@reversion.register()
class Institution(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(max_length=300, blank=True)
    authority_url = models.CharField(max_length=300, blank=True)
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250, blank=True,
        help_text="Alternative names",
        related_name="altname_of_inst"
    )
    abbreviation = models.CharField(max_length=300, blank=True)
    location = models.ForeignKey(
        Place, blank=True, null=True, on_delete=models.SET_NULL
    )
    parent_institution = models.ForeignKey(
        'Institution', blank=True, null=True, related_name='children_institutions',
        on_delete=models.SET_NULL
    )
    comment = models.TextField(blank=True)

    @classmethod
    def get_listview_url(self):
        return reverse('entities:institution_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:institution_create')

    def get_absolute_url(self):
        return reverse('entities:institution_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:institution_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:institution_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'entities:institution_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:institution_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def __str__(self):
        return "{}".format(self.written_name)


@reversion.register()
class Person(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(max_length=300, blank=True)
    written_name_leven = models.CharField(max_length=254, blank=True)
    forename = models.CharField(max_length=300, blank=True)
    gender = models.CharField(max_length=300, blank=True)
    name = models.CharField(max_length=300, blank=True)
    house_name = models.CharField(max_length=300, blank=True)
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250, blank=True,
        help_text="Alternative names",
        related_name="altname_of_persons"
    )
    profession = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="Beruf(e)",
        related_name="is_profession_of"
    )
    belongs_to_place = models.ManyToManyField(
        Place, blank=True,
        related_name="living_place_for",
        verbose_name="Wohn- und Wirkungsort(e)",
    )
    place_of_birth = models.ForeignKey(
        Place, blank=True, null=True, related_name="is_birthplace",
        verbose_name="Geburtsort",
        on_delete=models.SET_NULL
    )
    place_of_death = models.ForeignKey(
        Place, blank=True, null=True, related_name="is_deathplace",
        verbose_name="Sterbeort",
        on_delete=models.SET_NULL
    )
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Geburtsdatum",
        help_text="YYYY-MM-DD"
    )
    date_of_death = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Sterbedatum",
        help_text="YYYY-MM-DD"
    )
    belongs_to_institution = models.ForeignKey(
        Institution, blank=True, null=True, related_name="has_member",
        on_delete=models.SET_NULL
    )
    comment = models.TextField(blank=True)
    is_main = models.BooleanField(
        blank=True, null=True,
        verbose_name="Name (Erklärung aus Verfachbuch)",
        help_text="Identifizierbare Personen, die im Eintrag erwähnt werden."
    )
    is_adm = models.BooleanField(
        blank=True, null=True,
        verbose_name="Beteiligte (administrative) Personen",
        help_text="Beteiligte Personen (Beamte, Gerichtsverpflichtete, Zeugen, ...).",
    )
    is_related = models.BooleanField(
        blank=True, null=True,
        verbose_name="Beteiligte (nicht-administrative) Personen",
        help_text="Beteiligte Personen (Erbsinteressenten, Gerhaben, Anweiser,\
        Verkäufer, Verpächter, Käufer, Pächter, ...)."
    )
    is_other = models.BooleanField(
        blank=True, null=True,
        verbose_name="Sonstig genannte Personen",
        help_text="Sonstig genannte Personen.",
    )

    class Meta:
        ordering = ['id']

    @classmethod
    def get_listview_url(self):
        return reverse('entities:person_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:person_create')

    def get_absolute_url(self):
        return reverse('entities:person_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('entities:person_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:person_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:person_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'entities:person_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:person_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def get_family(self):
        ct = ContentType.objects.get(app_label='entities', model='personperson').model_class()
        active = ct.objects.filter(source=self)
        inverse = ct.objects.filter(target=self)
        return {
            "active": active,
            "inverse": inverse
        }

    def __str__(self):
        if self.written_name:
            return "{}".format(self.written_name)
        elif self.name and self.forename:
            return "{}, {}".format(self.name, self.forename)
        elif self.name:
            return "{}".format(self.name)
        else:
            return "No name provided"


class PersonPerson(IdProvider):
    source = models.ForeignKey(
        Person, blank=True, null=True,
        related_name="has_person_a",
        verbose_name="Person A",
        on_delete=models.SET_NULL
    )
    target = models.ForeignKey(
        Person, blank=True, null=True,
        related_name="has_person_b",
        verbose_name="Person B",
        on_delete=models.SET_NULL
    )
    rel_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Art der Verbindung",
        related_name="relation_type",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "{} {} {}".format(self.source, self.rel_type, self.target)

    @classmethod
    def get_listview_url(self):
        return reverse('entities:personperson_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:personperson_create')

    def get_absolute_url(self):
        return reverse('entities:personperson_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('entities:personperson_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:personperson_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:personperson_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'entities:personperson_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:personperson_detail',
                kwargs={'pk': prev.first().id}
            )
        return False


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
        return reverse('entities:work_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:work_create')

    def get_absolute_url(self):
        return reverse('entities:work_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('entities:work_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:work_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:work_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'entities:work_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:work_detail',
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
