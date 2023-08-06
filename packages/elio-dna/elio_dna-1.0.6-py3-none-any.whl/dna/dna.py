"""DnaOfDjangoModel: Return the DNA of django models.

This class builds a python dict we can use to replicate Django models.

The dictionary is a cacheable/pickle friendly object which can be passed to the
`ReplicateDjangoModel` methods. Having this in another layer allows us to store
it and also peek at it which is helpful for debugging.

**Usage**

::

    from dna.dna import DnaOfDjangoModel

    dna = DnaOfDjangoModel("schema.jsonld", site_dna, type_depth)
    replicate_dna = dna.build()"""
# -*- encoding: utf-8 -*
import hashlib
import json
from django.db import models
from django.conf import settings
from django.urls import reverse
from dna.crispr import Crispr
from apep.picklejar import PickleJar


class DnaOfDjangoModel:
    """Build the DNA of django models from the Crispr."""

    def __init__(
        self,
        schema_path,
        site_dna,
        type_depth,
        domain="http://schema.org",
        no_comments=False,
    ):
        # How deep to use class types
        self.type_depth = type_depth
        # A map of the site
        self.site_dna = site_dna
        # Convert schema.org jsonld information into parsable units.
        self.crispr = Crispr(schema_path, domain=domain)
        # Remove comments from the build.
        self.no_comments = no_comments
        # Holding places for the structure `DnaOfDjangoModel` builds.
        self._replicate_dna = dict()
        self._backbone = list()
        self._iterables = set()
        self._site_things = dict()
        self._thing_names = set()

    @property
    def domain(self):
        """The schema's domain."""
        return self.crispr.domain

    @property
    def replicate_dna(self):
        return self._replicate_dna

    @property
    def backbone(self):
        return [self.crispr.name_from_url(b) for b in self._backbone]

    @property
    def iterables(self):
        return self._iterables

    @property
    def site_things(self):
        return self._site_things

    @staticmethod
    def dna_of_model_field_type_selector(first_type_in, this_list):
        """Gets the first type which matches the list."""
        for type in first_type_in:
            if type in this_list:
                return type
        return None

    def dna_of_model_field_type(self, thing_name, prp):
        """Selects the best django field Type for any property.

        This works on a sliding scale: Taking the first Type which matches if
        the Property has many.

        1. Use the property_name against predefined lists.
        2. Use the Property Enumerated if Enumerated Type is in dependencies.
        3. Use a Class Type if the Class Type is already in dependencies.
        4. Use the first Django Field for Primitive or semi-Primitive.
        5. Use a DJANGO_FIELDS for Primitive Types.
        6. Use Text by default.
        """
        property_name = Crispr.property_name(prp)
        IMAGEFIELD = dict(
            blank=True,
            field_type="ImageField",
            upload_to=f"images/{thing_name}/{property_name}",
            null=True,
        )
        FILEFIELD = dict(
            blank=True,
            field_type="FileField",
            upload_to=f"files/{thing_name}/{property_name}",
            null=True,
        )
        MONEYFIELD = dict(
            decimal_places=2, field_type="DecimalField", max_digits=10
        )

        # Beware 1. The order here is important. Types are selected first come.
        # Beware 2. No field should *python-by-reference* the same Type.
        DJANGO_FIELDS = {
            "Boolean": dict(
                blank=False,
                default=False,
                field_type="BooleanField",
                null=False,
            ),
            "Time": dict(blank=True, field_type="TimeField", null=True),
            "DateTime": dict(blank=True, field_type="DateTimeField", null=True),
            "Date": dict(blank=True, field_type="DateField", null=True),
            "Number": dict(
                blank=True, default=0, field_type="FloatField", null=True
            ),
            "Integer": dict(
                blank=True, default=0, field_type="IntegerField", null=True
            ),
            "Float": dict(
                decimal_places=10, field_type="DecimalField", max_digits=19
            ),
            "Quantity": dict(
                blank=True, default=0, field_type="FloatField", null=True
            ),
            "Duration": dict(blank=True, field_type="DurationField", null=True),
            "URL": dict(
                blank=True, field_type="URLField", max_length=512, null=True
            ),
            "email": dict(field_type="EmailField"),
            "image": IMAGEFIELD,
            "logo": IMAGEFIELD,
            "screenshot": IMAGEFIELD,
            "beforeMedia": FILEFIELD,
            "afterMedia": FILEFIELD,
            "duringMedia": FILEFIELD,
            "minPrice": MONEYFIELD,
            "maxPrice": MONEYFIELD,
            "price": MONEYFIELD,
            "minValue": MONEYFIELD,
            "value": MONEYFIELD,
            "maxValue": MONEYFIELD,
        }
        property_types = self.crispr.property_types_of(prp, self.domain)
        type = None  # Currently unknown.
        # Is there a matching Class Type?
        class_type = DnaOfDjangoModel.dna_of_model_field_type_selector(
            [t for t in property_types if not t.endswith("/Text")],
            [t for t in self._backbone if t not in self.crispr.primitives],
        )
        enumerated_type = self.crispr.property_enumerated(
            prp, settings.DNA_ENUMERATION_MODEL_NAME
        )
        choices = self.crispr.enumerations_of_by_url(enumerated_type)
        if enumerated_type and class_type and choices:
            # Type Enumerated
            return dict(
                default=choices[0][0],
                choices=choices,
                field_type="CharField",
                help_text="" if self.no_comments else prp["rdfs:comment"],
                max_length=len(max([c[0] for c in choices], key=len)),
            )
        if class_type:
            # Use the Class Type
            type = class_type
        if not type:
            # Try a Django Model
            type = DnaOfDjangoModel.dna_of_model_field_type_selector(
                [f"{self.domain}/{t}" for t in DJANGO_FIELDS.keys()],
                [t for t in property_types if not "Text" in t],
            )
        if not type:
            # Try a Primitive Type - leave Text til last
            type = DnaOfDjangoModel.dna_of_model_field_type_selector(
                [t for t in property_types if not "Text" in t], self._backbone
            )
        if not type:
            # Fall back to Text
            type = f"{self.domain}/Text"
        # Get the name
        type_name = self.crispr.name_from_url(type)
        # Now decide on the best django model Type
        django_type = None
        # Name of the property prefect for a known django model Type.
        if property_name in DJANGO_FIELDS.keys():
            django_type = DJANGO_FIELDS[property_name]
        # Name of the property preordained for long text.
        elif property_name in settings.DNA_LONG_TEXT_FIELDS:
            django_type = dict(blank=True, field_type="TextField")
        # Name of the property preordained char length.
        elif property_name in settings.DNA_SHORT_TEXT_FIELDS.keys():
            django_type = dict(
                blank=True,
                field_type="CharField",
                max_length=settings.DNA_SHORT_TEXT_FIELDS[property_name],
            )
        # Type matches a known django model Type.
        elif type_name in DJANGO_FIELDS.keys():
            django_type = DJANGO_FIELDS[type_name]
        # Standard Text Type.
        elif type_name == "Text":
            django_type = dict(
                blank=True, field_type="CharField", max_length=255
            )
        # ForeignKey to another schema Type.
        else:
            django_type = dict(
                blank=True,
                field_type="ForeignKey",
                null=True,
                related_name=f"{settings.APP_NAME}_{type_name}_{thing_name}_{property_name}".lower(),
                related_to=type_name,  # f"{settings.APP_NAME.title()}{type_name}",
            )
        django_type["help_text"] = (
            "" if self.no_comments else prp["rdfs:comment"]
        )
        return django_type

    def dna_of_model_fields(self, thing_name, thing_properties):
        """Return the django fields converted from the properties of a model.

        :param thing_name: e.g. "AppnameThing"
        :param thing_properties: e.g.
            [{
                '@id': 'http://schema.org/sameAs',
                '@type': 'rdf:Property',
                'http://schema.org/domainIncludes': {'@id': 'http://schema.org/Thing'},
                'http://schema.org/rangeIncludes': {'@id': 'http://schema.org/URL'},
                'rdfs:comment': "Comment...",
                'rdfs:label': 'sameAs'
            }, {
                '@id': 'http://schema.org/url',
                '@type': 'rdf:Property',
                'http://schema.org/domainIncludes': {'@id': 'http://schema.org/Thing'},
                'http://schema.org/rangeIncludes': {'@id': 'http://schema.org/URL'},
                'rdfs:comment': 'URL of the item.',
                'rdfs:label': 'url'
            }, ...]
        """
        fields = dict()
        for prp in thing_properties:
            fields[Crispr.property_name(prp)] = self.dna_of_model_field_type(
                thing_name, prp
            )
        return fields

    def model_inherits_fields(self, immediately_inherits_from):
        """All fields a model will inherit given its immediate inheritance."""
        inherits_fields = []
        for inheritance in immediately_inherits_from:
            if not inheritance == "models.Model":
                inheritance_dna = self._replicate_dna[inheritance]
                inherits_fields += inheritance_dna["fields_of"].keys()
                inherits_fields += self.model_inherits_fields(
                    inheritance_dna["inherits_from"]
                )
        return inherits_fields

    def model_inherits_from(self, class_of_thing):
        """Return which django model this sub class should inherit from.

        :param class_of_thing: e.g.
            {
              "@id": "http://schema.org/CafeOrCoffeeShop",
              "@type": "rdfs:Class",
              "rdfs:comment": "A cafe or coffee shop.",
              "rdfs:label": "CafeOrCoffeeShop",
              "rdfs:subClassOf": {
                "@id": "http://schema.org/FoodEstablishment"
              }
            }
        """
        # Assume this thing inherits from the base Model (only Thing does!)
        inherits_from = ["models.Model"]
        subclasses_things = Crispr.subclasses_direct(class_of_thing)
        if subclasses_things:
            inherits_from = []
            for subclasses in subclasses_things:
                model_dna = self.dna_of_model(
                    self.crispr.class_of_by_url(subclasses)
                )
                inherits_from.append(model_dna["thing_name"])
        return inherits_from

    def dna_of_model_exists(self, thing_name):
        """Utility to determine if the thing_name exists in our structure."""
        return thing_name in [m for m in self._replicate_dna.keys()]

    def dna_of_model_if_exists(self, thing_name):
        """Utility to get an existing django model if has already been built."""
        model = None
        if self.dna_of_model_exists(thing_name):
            model = self._replicate_dna[thing_name]
        return model

    def dna_of_model(self, class_of_thing, options=None):
        """Return a django model given a class object.

        :param class_of_thing: e.g.
            {
                '@id': 'http://schema.org/Thing',
                '@type': 'rdfs:Class',
                'rdfs:comment': 'The most generic type of item.',
                'rdfs:label': 'Thing'
            }
        """
        thing_name = class_of_thing.get("rdfs:label")
        if isinstance(thing_name, dict):
            thing_name = thing_name.get("@value")
        # thing_name = f"{settings.APP_NAME.title()}{thing_name}"
        # Simply return dna of models we have already created (i.e. inherit from).
        model = self.dna_of_model_if_exists(thing_name)
        if model:
            return model
        # Fields
        fields_of = self.dna_of_model_fields(
            thing_name, self.crispr.properties_of_by_url(class_of_thing["@id"])
        )
        # Establish all the inheritance from other things
        inherits_from = self.model_inherits_from(class_of_thing)
        # Remove fields inherited from parent classes (it's possible because in
        # schema a child class inherits from 2 classes - and any of them
        # are optional - so schema shows properties in the child class that
        # should be present even if you opt not to inherit one of the parents
        # with it).
        all_parent_fields = set(self.model_inherits_fields(inherits_from))
        names_existing = all_parent_fields.intersection(set(fields_of))
        if names_existing:
            for field_name in names_existing:
                fields_of.pop(field_name)
        # Switch _iterables into Many2Many
        iterable_fields = dict()
        for field_name, field_dna in fields_of.items():

            if field_name in self._iterables:
                iterable_fields[field_name] = field_dna.copy()
                if field_dna["field_type"] == "ForeignKey":
                    del iterable_fields[field_name]["blank"]
                    del iterable_fields[field_name]["null"]
                    del iterable_fields[field_name]["related_name"]
                else:
                    iterable_fields[field_name] = dict(
                        field_type="ForeignKey",
                        related_to=settings.DNA_BASE_MODEL_NAME,  # f"{settings.APP_NAME.title()}Thing",
                    )
        # Build the dict
        model_dict = {
            "fields_of": fields_of,
            "inherits_from": inherits_from,
            "thing_name": thing_name,
            "iterables": iterable_fields,
        }
        # Keep track of the dna of models and fields we have created.
        self._replicate_dna[thing_name] = model_dict
        return model_dict

    def _get_things_of_site(self, site_dna, thing_names=None):
        """Recursively extract all the model Thing Types from the SITE_DNA."""
        if not thing_names:
            thing_names = {settings.DNA_BASE_MODEL_NAME}
        for key, value in site_dna.items():
            if isinstance(value, dict):
                # Fetch "Things Types" hosted in "engage" and "list" keys.
                for elio_type in ["engage", "list"]:
                    for each_thing in list(value.get(elio_type, {})):
                        self._site_things[key] = {
                            each_thing: value.get(elio_type, {}).copy()
                        }
                        thing_names.add(each_thing)
                # Thing properties hosted in the "many" key should be listed
                # as Many2Many objects.
                iterate_properties = value.get("many", [])
                for each_property in iterate_properties:
                    self._iterables.add(each_property)
                    prop = self.crispr.property_of_by_name(each_property)
                    # Look for non-primitive "Thing Types".
                    prop_types = Crispr.property_types_of(prop, self.domain)
                    prim_types = self.crispr.primitive_types_of(prop_types)
                    # "Thing Types" when more Types than just Primitive.
                    thing_types = set(prop_types).difference(set(prim_types))
                    for thing_type in thing_types:
                        thing_names.add(self.crispr.name_from_url(thing_type))
                # Recusively look for more Types.
                thing_names.union(self._get_things_of_site(value, thing_names))
        return thing_names

    def _get_replicate_dna(self, backbone):
        """Build all the DNA of models listed in the backbone."""
        # Do each model in any order: `dna_of_model` will do ancestors first.
        for thing_url in self._backbone:
            class_of = self.crispr.class_of_by_url(thing_url)
            self.dna_of_model(class_of)
        return self._replicate_dna

    def build(self):
        """Main build method."""
        site_dna_dump = json.dumps(self.site_dna, sort_keys=True)
        picklename = hashlib.sha1(
            f"{site_dna_dump}{self.type_depth}".encode()
        ).hexdigest()
        pick = PickleJar(f"picklings/{settings.APP_NAME}", picklename[:200])
        # Return an existing DNA.
        if pick.ripe:
            dna_dna = pick.open()
            self._replicate_dna = dict(dna_dna["_replicate_dna"])
            self._backbone = list(dna_dna["_backbone"])
            self._iterables = set(dna_dna["_iterables"])
            self._site_things = dict(dna_dna["_site_things"])
            self._thing_names = list(dna_dna["_thing_names"])
            return self._replicate_dna
        # Get the list of all things the site_dna models mention.
        self._thing_names = self._get_things_of_site(self.site_dna)
        # Get the list of all things the site_dna models require.
        self._backbone = self.crispr.dependencies_of_by_names(
            list(self._thing_names), self.type_depth
        )
        # Get the DNA we can pass to the Replicate class
        self._replicate_dna = self._get_replicate_dna(self._backbone)
        # Pickle for next time
        pick.pickle(
            {
                "_replicate_dna": self._replicate_dna,
                "_site_things": self._site_things,
                "_iterables": list(self._iterables),
                "_thing_names": list(self._thing_names),
                "_backbone": self._backbone,
            }
        )
        return self._replicate_dna
