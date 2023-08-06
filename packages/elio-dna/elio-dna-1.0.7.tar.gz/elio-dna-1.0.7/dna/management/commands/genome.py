"""**Usage**

::

    # Show the full scheme of a Class or Property.
    django-admin genome Thing
    django-admin genome description"""
# -*- encoding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from dna.crispr import Crispr


class Command(BaseCommand):
    """Build a mock file you can use to test with from a Thing."""

    def add_arguments(self, parser):
        """
        :param name: Something to .
        """
        parser.add_argument("name", type=str, help="A thing to examine")
        parser.add_argument(
            "-d",
            "--dependants",
            dest="show_deps",
            action="store_true",
            help="Show dependants.",
        )
        parser.set_defaults(show_deps=False)

    def genome_comment(self, obj):
        comment = obj["rdfs:comment"]
        self.stdout.write(comment)

    def enumerated_genome(self, enumerations):
        if enumerations:
            self.stdout.write("Enumerated:")
            for enum in sorted(enumerations):
                self.stdout.write(f" |- {enum}")

    def subclasses_genome(self, subclasses):
        if subclasses:
            self.stdout.write("Subclasses:")
            for sub in sorted(subclasses):
                self.stdout.write(f" |- {sub}")

    def properties_genome(self, properties):
        if properties:
            self.stdout.write("Properties:")
            for prop_name in sorted(
                [Crispr.property_name(p) for p in properties]
            ):
                self.stdout.write(f" |- {prop_name}")

    def dependants_dependants_print(self, dependants, level):
        if isinstance(dependants, list):
            for sub in dependants:
                self.dependants_dependants_print(sub, level + 1)
        else:
            space = "   " * level
            self.stdout.write(f"{space}|- {dependants}")

    def dependants_genome(self, dependants):
        if dependants:
            self.stdout.write("Dependants:")
            self.dependants_dependants_print(dependants, 0)

    def handle(self, *args, **options):
        name = options["name"]
        show_deps = options["show_deps"]
        crispr = Crispr(
            f"schemaorg/data/releases/{settings.SCHEMA_VERSION}/all-layers.jsonld"
        )

        property_of = None
        class_of = crispr.class_of_by_name(name)
        if not class_of:
            property_of = crispr.property_of_by_name(name)

        if not property_of and not class_of:
            raise CommandError(f"{name} not found.")

        if property_of:
            self.stdout.write(f"Property: {name}")
            self.genome_comment(property_of)
            self.stdout.write("Types:")
            for type in crispr.property_types_of(property_of, crispr.domain):
                self.stdout.write(f" |- {type}")
            self.stdout.write("Classes:")
            for cls in crispr.property_domains_of(property_of, crispr.domain):
                self.stdout.write(f" |- {cls}")

            self.enumerated_genome(
                crispr.enumerations_of_by_url(
                    crispr.property_enumerated(
                        property_of, settings.DNA_ENUMERATION_MODEL_NAME
                    )
                )
            )

        if class_of:
            self.stdout.write(f"Class: {name}")
            self.genome_comment(class_of)
            if crispr.is_primitive_thing(class_of, crispr.domain):
                self.stdout.write(" |- PRIMITIVE TYPE")
            # self.stdout.write(str(class_of))
            self.subclasses_genome(crispr.subclasses_of(class_of))
            self.properties_genome(crispr.properties_of_by_name(name))
            self.enumerated_genome(crispr.enumerations_of_by_name(name))
            if show_deps:
                self.dependants_genome(crispr.descendants_of_by_name(name))
