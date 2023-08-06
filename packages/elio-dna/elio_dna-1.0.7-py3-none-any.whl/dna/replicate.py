"""ReplicateDjangoModel: Return django models.

This class builds dynamic Django models the DNA of schema.org "Things".

Initialize with the product of `DnaOfDjangoModel`.`_get_replicate_dna`. The
`start_replication` method will build each Django model which will be registered
as if hand coded in a models.py file. You will be able to run `makemigrations`
and  `migrate` as usual.


**Usage**

::

    from dna.dna import DnaOfDjangoModel
    from dna.replicate import ReplicateDjangoModel

    # First build or retrieve from storage the DNA of models.
    dna_maker = DnaOfDjangoModel("schema.jsonld", "app")
    dna = dna_maker._get_replicate_dna(<SITE_DNA>, 1)

    # Then instantiate this class and start the model registration.
    replicator = ReplicateDjangoModel(dna, "app")
    replicator.start_replication()"""
# -*- encoding: utf-8 -*
from django.conf import settings
from django.db import models
from django.urls import resolve, reverse_lazy
from polymorphic.models import PolymorphicModel
from slugify.slugify import slugify


class ReplicateDjangoModel:
    """Build django models from the DNA."""

    def __init__(self, model_dna):
        # Schema.org jsonld information as parsable units.
        self.dna = model_dna
        # Holding places for the structure `ReplicateDjangoModel` builds.
        self.models_loaded = {"models.Model": PolymorphicModel}

    def get_model_field_dynamically(self, dna_of_field):
        """Returns an instance of a django model type."""
        field_type = dna_of_field.pop("field_type")
        if field_type == "ForeignKey":
            related_to = dna_of_field.pop("related_to")
            dna_of_field["on_delete"] = models.CASCADE
            return models.ForeignKey(related_to, **dna_of_field)
        else:
            django_model_type = getattr(models, field_type)
            return django_model_type(**dna_of_field)

    def get_model_inheritance(self, inherit_from):
        """Get or create a model required for inheritance."""
        model_inheritance = self.models_loaded.get(inherit_from, None)
        if not model_inheritance:
            model_inheritance = self.replicate_django_model(
                inherit_from, self.dna[inherit_from]
            )
        return model_inheritance

    def replicate_django_model(self, thing_name, dna_of_model, options=None):
        """Return a django model given a class object.

        :param dna_of_model: e.g.
            {
                "fields_of": {
                    "name": {
                        "field_type": "CharField",
                        "max_length": 512,
                        "blank": true,
                    },
                    "identifier": {
                        "blank": true,
                        "field_type": "ForeignKey",
                        "related_name": "dnathing_dnacreativework_about",
                        "related_to": "Thing",
                        "null": true,
                    },
                    "description": {"field_type": "TextField", "blank": true},
                },
                "inherits_from": ["base.Model"],
                "thing_name": "AppnameThing",
            }
        """
        # Don't keep getting the same model over and over.
        model = self.models_loaded.get(thing_name, None)
        if model:
            return model

        class Meta:
            db_table = thing_name
            app_label = settings.APP_NAME

        def get_host_page(self):
            return self.elio_page

        def get_absolute_url(self):
            return reverse_lazy(
                "engage.thing",
                kwargs={
                    "page_slug": slugify(self.thing_name),
                    "thing": self.thing_name,
                    "pk": self.pk,
                },
            )

        def get_fields(self):
            return [
                (field.name, type(field).__name__, getattr(self, field.name))
                for field in self._meta.fields
                if type(field).__name__ not in ["ImageField", "FileField"]
            ]

        def get_images(self):
            # Get all the image fields
            images = [
                (field, self)
                for field in self._meta.fields
                if type(field).__name__ in ["ImageField"]
            ]
            # Return only images with images.
            return [
                (i[0].name, i[1].image.url, i[1].image.height, i[1].image.width)
                for i in images
                if i[1].image
            ]

        def __str__(self):
            return self.name

        # Update Meta with any options that were provided
        if options is not None:
            for key, value in options.iteritems():
                setattr(Meta, key, value)

        # Set up a dictionary to simulate declarations within a class
        attrs = {
            "__module__": __name__,
            "__str__": __str__,
            "Meta": Meta,
            "get_absolute_url": get_absolute_url,
            "get_host_page": get_host_page,
            "get_fields": get_fields,
            "get_images": get_images,
            "thing_name": thing_name,
        }
        # Model Inheritance.
        inheritance = []
        for inherit_from in dna_of_model["inherits_from"]:
            model_inheritance = self.get_model_inheritance(inherit_from)
            inheritance.append(model_inheritance)

        # Fields.
        for field_name, dna_of_field in dna_of_model["fields_of"].items():
            attrs[field_name] = self.get_model_field_dynamically(dna_of_field)
        # Add some additional system fields.
        if thing_name == settings.DNA_BASE_MODEL_NAME:
            attrs["elio_key"] = models.SlugField(max_length=128, unique=False)
            attrs["elio_page"] = models.CharField(
                blank=True, max_length=128, null=True
            )
            attrs["elio_role"] = models.CharField(
                blank=False, max_length=8, null=False, default="list"
            )
        # Manually create the inheritance pointer.
        for point_to in inheritance:
            if not point_to.__name__ == "PolymorphicModel":
                attrs[
                    f"{thing_name}_to_{point_to.__name__}".lower()
                ] = models.OneToOneField(
                    f"{point_to.__name__}",
                    parent_link=True,
                    related_name=f"{point_to.__name__}_for_{thing_name}",
                    on_delete=models.CASCADE,
                )
        # Create the class, which automatically triggers ModelBase processing.
        model = type(thing_name, tuple(inheritance), attrs)
        # Store it so that we can pick it up for inheritance.
        self.models_loaded[thing_name] = model
        # Return the model.
        return model

    def start_replication(self):
        """Build all the models."""
        # Do each model in any order
        for thing_name, model_dna in self.dna.items():
            self.replicate_django_model(thing_name, model_dna)
