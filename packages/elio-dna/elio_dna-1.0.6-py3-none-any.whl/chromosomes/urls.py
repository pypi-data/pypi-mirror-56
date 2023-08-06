# -*- encoding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    ViewEveryThing,
    ChromosomesCreateView,
    ChromosomesDeleteView,
    ChromosomesDetailView,
    ChromosomesListView,
    ChromosomesUpdateView,
)


urlpatterns = [
    path("", ViewEveryThing.as_view(app_name="Chromosomes"), name="things"),
    path(
        "create/<str:thing_name>",
        ChromosomesCreateView.as_view(app_name="Chromosomes"),
        name="create.thing",
    ),
    path(
        "delete/<str:thing_name>/<int:pk>",
        ChromosomesDeleteView.as_view(app_name="Chromosomes"),
        name="delete.thing",
    ),
    path(
        "engage/<str:thing_name>/<int:pk>",
        ChromosomesDetailView.as_view(app_name="Chromosomes"),
        name="engage.thing",
    ),
    path(
        "list/<str:thing_name>/",
        ChromosomesListView.as_view(app_name="Chromosomes"),
        name="list.things",
    ),
    path(
        "update/<str:thing_name>/<int:pk>",
        ChromosomesUpdateView.as_view(app_name="Chromosomes"),
        name="update.thing",
    ),
]


if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
