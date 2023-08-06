# -*- encoding: utf-8 -*-
from django.conf import settings
from dna.dna import DnaOfDjangoModel
from dna.replicate import every_model, eliolist_model


dna = DnaOfDjangoModel(
    settings.SCHEMA_PATH, "chromosomes", elio_list=settings.ELIO_LIST
).dna_of_models(list(settings.SITE_DNA), settings.DNA_DEPTH)

every_model(dna, "chromosomes")
