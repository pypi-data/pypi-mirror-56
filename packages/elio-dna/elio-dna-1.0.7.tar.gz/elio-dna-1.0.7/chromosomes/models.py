# -*- encoding: utf-8 -*-
from django.conf import settings
from dna.dna import DnaOfDjangoModel
from dna.models import every_model, eliomany_model


every_model(
    DnaOfDjangoModel(
        settings.SCHEMA_PATH, settings.SITE_DNA, settings.DNA_DEPTH
    ).build()
)

eliomany_model()
