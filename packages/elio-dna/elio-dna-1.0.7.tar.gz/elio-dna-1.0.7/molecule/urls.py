# -*- encoding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import Criew, Uiew, Diew, Eiew, Liew, Miew, Oiew, Piew, Hiew


urlpatterns = [
    path(
        "cr/<str:page_slug>/<str:role>/<str:thing>",
        Criew.as_view(),
        name="create.thing",
    ),
    path(
        "u/<str:page_slug>/<str:role>/<str:thing>/<int:pk>",
        Uiew.as_view(),
        name="update.thing",
    ),
    path(
        "d/<str:page_slug>/<str:thing>/<int:pk>",
        Diew.as_view(),
        name="delete.thing",
    ),
    path(
        "e/<str:page_slug>/<str:thing>/<int:pk>",
        Eiew.as_view(),
        name="engage.thing",
    ),
    path("l/<str:page_slug>/<str:thing>", Liew.as_view(), name="list.things"),
    path(
        "m/<str:page_slug>/<str:thing>/<int:pk>/<str:prop>",
        Miew.as_view(),
        name="many.things",
    ),
    path(
        "o/<str:page_slug>/<str:thing>", Oiew.as_view(), name="optimize.things"
    ),
    path("p/<str:page_slug>", Piew.as_view(), name="engage.page"),
    path("", Hiew.as_view(), name="splash"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
