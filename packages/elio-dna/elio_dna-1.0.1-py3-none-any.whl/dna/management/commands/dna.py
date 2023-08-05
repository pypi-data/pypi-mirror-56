"""**Usage**

::

    # Show the full dna in advance
    django-admin dna Thing Person -d 0"""
# -*- encoding: utf-8 -*-
import json
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from dna.dna import DnaOfDjangoModel


class Command(BaseCommand):
    """Build the dna of models you can use to build django Models from."""

    def add_arguments(self, parser):
        """
        :param name: things.
        """
        parser.add_argument(
            "things", nargs="+", type=str, help="Space delimited list of things"
        )
        parser.add_argument(
            "--depth",
            "-d",
            type=int,
            help="Max depth to accept object types for properties.",
        )
        parser.add_argument(
            "--path", "-p", type=str, help="Path of the schema's jsonld."
        )

    def handle(self, *args, **options):
        names = options["things"]
        depth = options["depth"]
        schema_path = options["path"]
        dna = DnaOfDjangoModel(schema_path, app_label="dna", no_comments=True)
        dna._get_replicate_dna(names, depth)
        with open("dna.py", "w") as f:
            f.write(json.dumps(dna.dna_loaded, sort_keys=True, indent=4))
