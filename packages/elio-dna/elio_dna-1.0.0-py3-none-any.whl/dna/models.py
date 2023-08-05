# -*- encoding: utf-8 -*
from django.conf import settings
from django.db import models
from dna.replicate import ReplicateDjangoModel


def every_model(model_dna):
    """Utility function to build every model + the eliolist model."""
    replicator = ReplicateDjangoModel(model_dna)
    replicator.start_replication()


def eliolist_model():
    class ElioList(models.Model):
        parent_model = models.ForeignKey(
            "Thing", on_delete=models.CASCADE, related_name="parent_to_list"
        )
        listed_model = models.ForeignKey(
            "Thing", on_delete=models.CASCADE, related_name="listed_by_parent"
        )
        field_name = models.CharField(max_length=100)

        class Meta:
            db_table = "eliolist"
            app_label = settings.APP_NAME
            unique_together = ["parent_model", "listed_model", "field_name"]

    return ElioList
