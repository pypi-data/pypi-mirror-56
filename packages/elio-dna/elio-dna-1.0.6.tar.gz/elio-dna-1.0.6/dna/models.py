# -*- encoding: utf-8 -*
from django.apps import apps
from django.conf import settings
from django.db import models
from dna.replicate import ReplicateDjangoModel


def every_model(model_dna):
    """Utility function to build every model + the eliolist model."""
    replicator = ReplicateDjangoModel(model_dna)
    replicator.start_replication()


def eliomany_model():
    class ElioMany(models.Model):
        many_engaged = models.ForeignKey(
            settings.DNA_BASE_MODEL_NAME,
            on_delete=models.CASCADE,
            related_name="engaged_to_list",
        )
        many_listed = models.ForeignKey(
            settings.DNA_BASE_MODEL_NAME,
            on_delete=models.CASCADE,
            related_name="list_engaged",
        )
        engaged_thing = models.CharField(max_length=100)
        listed_thing = models.CharField(max_length=100)
        listed_field = models.CharField(max_length=100)
        elio_key = models.SlugField(max_length=128, unique=False)
        elio_page = models.CharField(blank=True, max_length=128, null=True)
        elio_role = models.CharField(
            blank=False, max_length=8, null=False, default="many"
        )

        class Meta:
            db_table = "eliomany"
            app_label = settings.APP_NAME
            unique_together = ["many_engaged", "many_listed", "listed_field"]

    return ElioMany


def EveryModel(model_name):
    return apps.get_model(model_name=model_name, app_label=settings.APP_NAME)
