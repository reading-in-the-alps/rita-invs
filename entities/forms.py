from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,  Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup
from .models import *


class PersonPersonFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonPersonFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'source',
                'target',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search',
                    'rel_type',
                    css_id="more"
                    ),
                )
            )


class PersonPersonForm(forms.ModelForm):
    class Meta:
        model = PersonPerson
        fields = "__all__"
        widgets = {
            'source': autocomplete.ModelSelect2(
                url='entities-ac:person-autocomplete'),
            'target': autocomplete.ModelSelect2(url='entities-ac:person-autocomplete'),
            'rel_type': autocomplete.ModelSelect2(
                url='/vocabs-ac/concept-by-colleciton-ac/fam-rel'),
        }

    def __init__(self, *args, **kwargs):
        super(PersonPersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class PersonFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                'forename',
                'written_name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Biographisches',
                    'belongs_to_place',
                    'belongs_to_place__name',
                    'profession',
                    'gender',
                    css_id="more"
                    ),
                AccordionGroup(
                    'Rolle',
                    'is_main',
                    'is_related',
                    'is_adm',
                    'is_other',
                    css_id="rolle"
                    ),
                AccordionGroup(
                    'Inventare & Bücher',
                    'is_main_person__buecher_sys',
                    'is_main_person__mentioned_books',
                    'is_main_person__mentioned_books__title',
                    'is_main_person__mentioned_books_nr',
                    css_id="inventare"
                    ),
                )
            )


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        widgets = {
            'belongs_to_institution': autocomplete.ModelSelect2(
                url='entities-ac:institution-autocomplete'),
            'place_of_birth': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'place_of_death': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'belongs_to_place': autocomplete.ModelSelect2Multiple(url='entities-ac:place-autocomplete'),
            'profession': autocomplete.ModelSelect2Multiple(
                url='/vocabs-ac/concept-by-colleciton-ac/Berufe'),
            'alt_names': autocomplete.ModelSelect2Multiple(
                url='entities-ac:altname-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class InstitutionFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InstitutionFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'written_name',
                'alt_names',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search',
                    'authority_url',
                    'location',
                    css_id="more"
                    ),
                )
            )


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = "__all__"
        widgets = {
            'location': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'parent_institution': autocomplete.ModelSelect2(
                url='entities-ac:institution-autocomplete'),
            'alt_names': autocomplete.ModelSelect2Multiple(
                url='entities-ac:altname-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(InstitutionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class AlternativeNameForm(forms.ModelForm):
    class Meta:
        model = AlternativeName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AlternativeNameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class AlternativeNameFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AlternativeNameFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search',
                    'name',
                    css_id="more"
                    ),
                )
            )


class AlternativeNameFormCreate(forms.ModelForm):
    class Meta:
        model = AlternativeName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AlternativeNameFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class PlaceFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PlaceFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search',
                    'geonames_id',
                    'part_of',
                    css_id="more"
                    ),
                )
            )


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {
            'part_of': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'alt_names': autocomplete.ModelSelect2Multiple(
                url='entities-ac:altname-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'save'),)


class PlaceFormCreate(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {
            'part_of': autocomplete.ModelSelect2(url='entities-ac:place-autocomplete'),
            'alt_names': autocomplete.ModelSelect2Multiple(
                url='entities-ac:altname-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(PlaceFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
