# -*- encoding: utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import (
    DateInput,
    DateTimeInput,
    HiddenInput,
    Select,
    TextInput,
    TimeInput,
)


class AnyEmailInput(TextInput):
    input_type = "email"


class AnyNumberInput(TextInput):
    input_type = "number"


class AnyTelephoneInput(TextInput):
    input_type = "tel"


class AnyDateInput(DateInput):
    input_type = "date"


class AnyDateTimeInput(DateTimeInput):
    input_type = "datetime-local"


class AnyTimeInput(TimeInput):
    input_type = "time"


class AnyForeignKeyInput(Select):
    # TODO: Add an [+] button create a new class for this FK
    input_type = "foreign"


def every_form(any_model, elio_key, page_link, field_dna=[]):
    class EveryForm(ModelForm):
        def __init__(self, *args, **kw):
            super().__init__(*args, **kw)
            for f, v in self.fields.items():
                if v.__class__.__name__ == "DateField":
                    self.fields[f].widget = AnyDateInput()
                elif v.__class__.__name__ == "TimeField":
                    self.fields[f].widget = AnyTimeInput()
                elif v.__class__.__name__ == "DateTimeField":
                    self.fields[f].widget = AnyDateTimeInput()
                elif v.__class__.__name__ == "EmailField":
                    self.fields[f].widget = AnyEmailInput()
                elif v.__class__.__name__ == "ModelChoiceField":
                    # self.fields[f].widget = AnyForeignKeyInput()
                    # TODO: Add an [+] button create a new class for this FK
                    pass
                elif v.__class__.__name__ in [
                    "DurationField",
                    "FloatField",
                    "IntegerField",
                ]:
                    self.fields[f].widget = AnyNumberInput()
                elif v.__class__.__name__ in [
                    "CharField",
                    "URLField",
                    "BooleanField",
                    "ImageField",
                    "TypedChoiceField",
                ]:
                    pass
                else:
                    print("Needs widget?", v.__class__.__name__)
            self.fields["elio_key"].widget = HiddenInput()
            self.fields["elio_key"].initial = elio_key
            self.fields["elio_page"].widget = HiddenInput()
            self.fields["elio_page"].initial = page_link

        field_order = [
            "name",
            "alternateName",
            "disambiguatingDescription",
            "image",
            "description",
            "sameAs",
        ]

        class Meta:
            model = any_model
            exclude = ["pk", "polymorphic_ctype", "elio_role"]
            if field_dna:
                fields = field_dna + ["elio_key", "elio_page"]

    return EveryForm
