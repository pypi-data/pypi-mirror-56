"""Crispr: Process a schema.org jsonld file ready for django models.

This class extracts all the required information to build a set of dynamic
Django models.


**Usage**

::

    from dna.crispr import Crispr
    crispr = Crispr("schemaorg/data/releases/3.9/all-layers.jsonld")"""
# -*- encoding: utf-8 -*
import json


def get_schema(schema_file):
    """Utility to open and load a jsonld file."""
    with open(schema_file) as json_data:
        return json.load(json_data)


class Crispr:
    """Parse a schemaorg jsonld."""

    def __init__(self, schema_path, domain="http://schema.org"):
        self.data = get_schema(schema_path)
        self.domain = domain
        # Separate classes from properties in advance.
        self.classes = [
            cls
            for cls in self.data.get("@graph", [])
            if "rdfs:Class" in self.list_anyway(cls["@type"])
        ]
        self.properties = [
            prp
            for prp in self.data.get("@graph", [])
            if prp["@type"] == "rdf:Property"
        ]
        self.enumerated = [
            obj
            for obj in self.data.get("@graph", [])
            if obj not in self.classes + self.properties
        ]
        self.primitives = [
            prm["@id"]
            for prm in self.classes
            if Crispr.is_primitive_thing(prm, self.domain)
        ] + [
            # Sub classed primitives
            "http://schema.org/Duration",
            "http://schema.org/Float",
            "http://schema.org/Integer",
            "http://schema.org/Quantity",
            "http://schema.org/URL",
        ]

    @staticmethod
    def merge(list1, list2):
        """Merge two lists without duplication."""
        for l in list2:
            if l not in list1:
                list1.append(l)
        return list1

    @staticmethod
    def list_anyway(obj):
        """Some values are lists, some dictionaries. Meh. List anyway."""
        if isinstance(obj, list):
            return obj
        else:
            return [obj]

    @staticmethod
    def is_of(obj, thing_url):
        """This is not the thing you are looking for."""
        return obj.get("@id") == thing_url

    @staticmethod
    def property_types_of(prp, domain):
        """Get all the Types supported by this Property."""
        types = []
        typesof = prp.get(f"{domain}/rangeIncludes", [])
        for range in Crispr.list_anyway(typesof):
            types.append(range["@id"])
        return types

    @staticmethod
    def property_domains_of(prp, domain):
        """Get all the Classes this Property belongs."""
        classes = []
        classesof = prp.get(f"{domain}/domainIncludes", [])
        for range in Crispr.list_anyway(classesof):
            classes.append(range["@id"])
        return classes

    @staticmethod
    def is_primitive_thing(cls, domain):
        """Check whether this Thing is a Primitive data type."""
        return f"{domain}/DataType" in Crispr.list_anyway(cls["@type"])

    @staticmethod
    def subclasses_direct(cls):
        if not cls:
            return []
        subclassesof = cls.get("rdfs:subClassOf", [])
        return [sub["@id"] for sub in Crispr.list_anyway(subclassesof)]

    @staticmethod
    def property_name(prp):
        """Parse all the different ways a property name is represented."""
        prp_name = prp["rdfs:label"]
        if isinstance(prp_name, dict):
            return prp_name["@value"]
        elif isinstance(prp_name, list):
            en = [p["@value"] for p in list if p["@language"] == "en"]
            if en:
                return en[0]
            else:
                [p["@value"] for p in list][0]
        else:
            return prp_name

    def name_from_url(self, url):
        return url.replace(self.domain + "/", "")

    def property_of_by_name(self, property_name):
        return self.property_of_by_url(f"{self.domain}/{property_name}")

    def class_of_by_name(self, thing_name):
        return self.class_of_by_url(f"{self.domain}/{thing_name}")

    def properties_of_by_name(self, thing_name):
        return self.properties_of_by_url(f"{self.domain}/{thing_name}")

    def enumerations_of_by_name(self, thing_name):
        return self.enumerations_of_by_url(f"{self.domain}/{thing_name}")

    def descendants_of_by_name(self, thing_name):
        return self.dependants_of_by_url(f"{self.domain}/{thing_name}")

    def dependencies_of_by_names(
        self, thing_names, max_depth=0, collated_things=[]
    ):
        return self.class_dependencies_of(
            [f"{self.domain}/{t}" for t in thing_names],
            max_depth,
            collated_things,
        )

    def property_of_by_url(self, property_url):
        """Return the dict of a property object from schema, given its URL."""
        for prp in self.properties:
            if Crispr.is_of(prp, property_url):
                return prp
        return None

    def class_of_by_url(self, thing_url):
        """Return the dict of a class object from schema, given its URL."""
        for cls in self.classes:
            if Crispr.is_of(cls, thing_url):
                return cls
        return None

    def properties_of_by_url(self, thing_url):
        """Return a dict list of a property objects of a class from schema."""
        properties = []
        for prp in self.properties:
            property_for = prp.get(f"{self.domain}/domainIncludes", [])
            for domain in Crispr.list_anyway(property_for):
                if Crispr.is_of(domain, thing_url):
                    properties.append(prp)
        return properties

    def enumerations_of_by_url(self, thing_url):
        """Return a dict list of a enumerations of a class from schema."""
        enumerations = []
        for enum in self.enumerated:
            if enum["@type"] == thing_url:
                enumerations.append(enum["rdfs:label"])
        return tuple((e, e) for e in enumerations)

    def property_enumerated(self, prp, enumerator_type):
        """See if a property type is enumarated and return it."""
        property_types = Crispr.property_types_of(prp, self.domain)
        for thing_url in property_types:
            subclasses = self.subclasses_of(self.class_of_by_url(thing_url))
            if f"http://schema.org/{enumerator_type}" in subclasses:
                return thing_url
        return None

    def dependants_of_by_url(self, thing_url, max_level=1):
        """Get all the dependants of a class from schema."""
        dependants = []
        for cls in self.classes:
            if thing_url in Crispr.subclasses_direct(cls):
                dependant_url = cls["@id"]
                dependants.append(dependant_url)
                if max_level > 0:
                    more = self.dependants_of_by_url(
                        dependant_url, max_level - 1
                    )
                    if more:
                        dep = [self.name_from_url(d) for d in more]
                        # dependant_url = f"{dependant_url} {dep}"
                        dependants.append(dep)
        return dependants

    def subclasses_of(self, cls):
        subclasses = []
        for thing_url in Crispr.subclasses_direct(cls):
            Crispr.merge(subclasses, [thing_url])
            Crispr.merge(
                subclasses, self.subclasses_of(self.class_of_by_url(thing_url))
            )
        return subclasses

    def primitive_types_of(self, thing_urls):
        """Filter out types which aren't primitive."""
        primitives = []
        for thing_url in thing_urls:
            if thing_url in self.primitives:
                primitives.append(thing_url)
        return primitives

    def class_dependencies_of(
        self, thing_urls, max_depth=0, collated_things=[]
    ):
        """Returns a list of classes required for your desired things.

        To avoid having too many class types for properties, it will stop
        getting new property types after a certain depth.

        Recursive: In phases:

        - Phase1.1. Get all the ancestor classes required by the first set.
        - Phase1.2. Get all the properties required by all these classes.
        - Phase1.3. Get the classes of these properties.
        - Phase1.4. Pass any new found classes into Phase2.
        - Repeat for Phase2=>Phase(x).
        - Phase(x).3. Only get primitive classes after x>=max_depth Phases.

        Phase(x).3 insures that we don't need too many deeply nested ForeignKeys
        for Things we are collecting. At some point we'll just collect some Text
        or a Number for a property - which can be represented by a DB field
        type.

        Once you have finished, you can use this list of classes to build your
        models. If a certain "Thing" has a property type which is not listed by
        this function, you should swap it for a primitive type instead.
        """
        # Copy this phase's thing_urls as a starting point.
        phase_urls = [u for u in thing_urls]
        # Check each thing_url
        for thing_url in thing_urls:
            # Add the sub classes. This gives you the full model requirement
            # for this phase.
            ancestors = self.subclasses_of(self.class_of_by_url(thing_url))
            Crispr.merge(phase_urls, ancestors)
            # Get Property Types of thing + ancestors.
            for ancestor_url in ancestors + [thing_url]:
                # Check the Types of each thing's Properties.
                for prop in self.properties_of_by_url(ancestor_url):
                    property_types_of = Crispr.property_types_of(
                        prop, self.domain
                    )
                    # Prevent going any deeper.
                    if max_depth < 1:
                        # Remove non-primitive Types, if deep enough.
                        property_types_of = self.primitive_types_of(
                            property_types_of
                        )
                        """This greatly reduces the number of new Types."""
                    Crispr.merge(phase_urls, property_types_of)
        # Have we found new Types?
        newly_found = [u for u in phase_urls if u not in collated_things]
        if len(newly_found):
            # Start a new phase for just these new Types.
            return self.class_dependencies_of(
                newly_found,
                max_depth=max_depth - 1,
                collated_things=collated_things + newly_found,
            )
        else:
            # We've found them all!
            class_dependencies = Crispr.merge(collated_things, phase_urls)
            # Return all the non primitive things.
            return [
                t for t in class_dependencies if not t in self.primitives
            ]  # [t for t in class_dependencies if not t in self.primitives]
