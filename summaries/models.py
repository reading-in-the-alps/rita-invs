from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField

from idprovider.models import IdProvider
from entities.models import Institution, Person, Place
from vocabs.models import SkosConcept
from books.models import Work


class VerfachBuch(IdProvider):
    """ Beschreibt die Archivalie 'Verfachbuch' """
    signatur = models.CharField(
        max_length=250, blank=True, help_text="Vollzitat des Verfachbuches",
        verbose_name="Archivsignatur des Verfachbuches"
    )
    repo = models.ForeignKey(
        Institution, blank=True, null=True, related_name="has_verfachbuch",
        on_delete=models.SET_NULL,
        verbose_name="Archiv",
        help_text="Das Archiv in welchem das Verfachbuch eingesehen werden kann"
    )
    year = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Jahr",
        help_text="Verfachbuch des Jahres JJJJ"
    )

    @classmethod
    def get_listview_url(self):
        return reverse('summaries:verfachbuecher_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('summaries:verfachbuch_create')

    def get_absolute_url(self):
        return reverse('summaries:verfachbuch_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('summaries:verfachbuch_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('summaries:verfachbuch_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = VerfachBuch.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = VerfachBuch.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        if self.signatur:
            return "{}".format(self.signatur)
        else:
            return "{}".format(self.id)


BUECHER = (
    ('Bücher', 'Bücher'),
    ('keine Bücher', 'keine Bücher'),
)

MEHRERE_HAUPTPERSONEN = (
    ('nur eine Hauptperson', 'nur eine Hauptperson'),
    ('mehrere Personen', 'mehrere Personen')
)

VOLLSTAENDIG = (
    ('unklar', 'unklar'),
    ('unvollständig', 'unvollständig'),
)

SCHREIBUTENSIELIEN = (
    ('Lese- und Schreibsachen', 'Lese- und Schreibsachen'),
    ('keine Lese- und Schreibsachen', 'keine Lese- und Schreibsachen'),
)


class InventoryEntry(IdProvider):
    """Beschreibt ein Regest eines Inventars"""
    inv_signatur = models.CharField(
        max_length=550, blank=True, help_text="Vollzitat des Eintrages",
        verbose_name="Archivsignatur des Eintrages"
    )
    is_located_in = models.ForeignKey(
        VerfachBuch, blank=True, null=True, related_name="has_inventories",
        on_delete=models.SET_NULL,
        verbose_name="Übergeordenter Quellenbestand",
        help_text="Ist Teil des übergordneten Quellenbestands."
    )
    inv_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Art des Inventars",
        help_text="Welche Art von Inventar wurde in diesem Eintrag protokolliert",
        on_delete=models.SET_NULL
    )
    excel_row = JSONField(
        null=True, blank=True, verbose_name="Original Erfassung", help_text="Excel-Sheet Eintrag"
    )
    main_person = models.ManyToManyField(
        Person, blank=True,
        verbose_name="Name (Erklärung aus Verfachbuch)",
        help_text="Identifizierbare Personen, die im Eintrag erwähnt werden.",
        related_name="is_main_person"
    )
    main_person_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl der Hauptpersonen",
        help_text="Anzahl der Hauptpersonen"
    )
    adm_person = models.ManyToManyField(
        Person, blank=True,
        verbose_name="Beteiligte (administrative) Personen",
        help_text="Beteiligte Personen (Beamte, Gerichtsverpflichtete, Zeugen, ...).",
        related_name="is_adm_person"
    )
    adm_person_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl beteiligte (administrative) Personen",
        help_text="Anzahl der beteiligten Personen (Beamte, Gerichtsverpflichtete, Zeugen, ...)"
    )
    related_person = models.ManyToManyField(
        Person, blank=True,
        verbose_name="Beteiligte (nicht-administrative) Personen",
        help_text="Beteiligte Personen (Erbsinteressenten, Gerhaben, Anweiser,\
        Verkäufer, Verpächter, Käufer, Pächter, ...).",
        related_name="is_related_person"
    )
    related_person_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl der beteiligten (nicht-administrative) Personen",
        help_text="Anzal der beteiligten Personen (Erbsinteressenten, Gerhaben, Anweiser,\
        Verkäufer, Verpächter, Käufer, Pächter, ...)."
    )
    other_person = models.ManyToManyField(
        Person, blank=True,
        verbose_name="Sonstig genannte Personen",
        help_text="Sonstig genannte Personen.",
        related_name="is_other_person"
    )
    other_person_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl der sonstig genannten Personen",
        help_text="Anzahl der sonstig genannten Personen"
    )
    barschaft = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Barschaft (teilweise eigene Berechnung)",
        help_text="Barschaft (teilweise eigene Berechnung)"
    )
    invenatar_summe_norm_fl = models.IntegerField(
        blank=True, null=True,
        verbose_name="Inventarsumme normiert (Gulden)",
        help_text="Inventarsumme normiert (Gulden)"
    )
    invenatar_summe_norm_kr = models.FloatField(
        blank=True, null=True,
        verbose_name="Inventarsumme normiert (Kreuzer)",
        help_text="Inventarsumme normiert (Kreuzer)"
    )
    vor_passiva_fl = models.IntegerField(
        blank=True, null=True,
        verbose_name="vor Abzug Passiva (Gulden)",
        help_text="vor Abzug Passiva (Gulden)"
    )
    vor_passiva_kr = models.FloatField(
        blank=True, null=True,
        verbose_name="vor Abzug Passiva (Kreuzer)",
        help_text="vor Abzug Passiva (Kreuzer)"
    )
    nach_passiva_fl = models.IntegerField(
        blank=True, null=True,
        verbose_name="nach Abzug Passiva (Gulden)",
        help_text="nach Abzug Passiva (Gulden)"
    )
    nach_passiva_kr = models.FloatField(
        blank=True, null=True,
        verbose_name="nach Abzug Passiva (Kreuzer)",
        help_text="nach Abzug Passiva (Kreuzer)"
    )
    comment_b = models.TextField(
        blank=True, null=True,
        verbose_name="Kommentar zu Spalte B",
        help_text="Kommentar zu Spalte B"
    )
    comment_k = models.TextField(
        blank=True, null=True,
        verbose_name="Kommentar zu Spalte K",
        help_text="Kommentar zu Spalte K"
    )
    comment_a = models.TextField(
        blank=True, null=True,
        verbose_name="Kommentar zu Spalte A",
        help_text="Kommentar zu Spalte A"
    )
    only_one_person = models.CharField(
        blank=True, null=True, default="mehrere Personen",
        choices=MEHRERE_HAUPTPERSONEN, max_length=250,
        verbose_name="Eine oder mehrere Hauptpersonen?"
    )
    buecher = models.TextField(
        blank=True, null=True,
        verbose_name="Buch/Bücher",
        help_text="Buch/Bücher"
    )
    buecher_sys = models.CharField(
        blank=True, null=True, default="keine Bücher",
        choices=BUECHER, max_length=250,
        verbose_name="Bücher erwähnt?"
    )
    mentioned_books = models.ManyToManyField(
        Work, blank=True,
        verbose_name="Erwähnte Bücher",
        help_text="Bücher, die in den Inventaren erähnt wurden",
        related_name="is_related_work"
    )
    mentioned_books_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl der erwähnten Bücher",
        help_text="Anzahl der erwähnten Bücher"
    )
    vollstaendig = models.CharField(
        blank=True, null=True, default="unklar",
        verbose_name="Inventar vollständig?",
        choices=VOLLSTAENDIG, max_length=250,
    )

    @classmethod
    def get_listview_url(self):
        return reverse('summaries:inventory_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('summaries:inventory_create')

    def get_absolute_url(self):
        return reverse('summaries:inventory_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('summaries:inventory_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('summaries:inventory_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = InventoryEntry.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = InventoryEntry.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        if self.inv_signatur:
            return "{}".format(self.inv_signatur)
        else:
            return "{}".format(self.id)

    def save_stats(self, *args, **kwargs):
        self.main_person_nr = self.main_person.all().count()
        self.adm_person_nr = self.adm_person.all().count()
        self.related_person_nr = self.related_person.all().count()
        self.other_person_nr = self.other_person.all().count()
        if int(self.main_person_nr) == 1:
            self.only_one_person = "nur eine Hauptperson"
        self.save()
