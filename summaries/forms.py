from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import *

from . models import *


class InventoryEntryForm(forms.ModelForm):
    class Meta:
        model = InventoryEntry
        fields = "__all__"
        widgets = {
            'main_person': autocomplete.ModelSelect2Multiple(
                url='entities-ac:person-autocomplete'
            ),
            'adm_person': autocomplete.ModelSelect2Multiple(
                url='entities-ac:person-autocomplete'
            ),
            'related_person': autocomplete.ModelSelect2Multiple(
                url='entities-ac:person-autocomplete'
            ),
            'other_person': autocomplete.ModelSelect2Multiple(
                url='entities-ac:person-autocomplete'
            ),
        }

    def __init__(self, *args, **kwargs):
        super(InventoryEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class InventoryEntryFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InventoryEntryFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Suche in Signatur',
                    'inv_signatur',
                    'is_located_in__signatur',
                    css_id="basic_search_fields"
                    ),
                AccordionGroup(
                    'Suche im Inhalt',
                    'excel_row',
                    'only_one_person',
                    css_id="inhalt_search_fields"
                    ),
                AccordionGroup(
                    'Vermögen',
                    'invenatar_summe_norm_fl',
                    'vor_passiva_fl',
                    'nach_passiva_fl',
                    css_id="vermoegen"
                    ),
                AccordionGroup(
                    'Lesen & Schreiben',
                    'buecher',
                    'buecher_sys',
                    'mentioned_books',
                    'mentioned_books__title',
                    'vollstaendig',
                    css_id="lesen"
                    ),
                )
            )


class VerfachBuchForm(forms.ModelForm):
    class Meta:
        model = VerfachBuch
        fields = "__all__"


class VerfachBuchFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(VerfachBuchFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'signatur',
                    'year',
                    css_id="basic_search_fields"
                    ),
                )
            )
