# -*- encoding: utf-8 -*-
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from dna.view_mixins import (
    EveryThingMixin,
    EveryDeleteMixin,
    EveryQuerySetMixin,
    EveryGetObjectMixin,
    EveryEditMixin,
    EveryManyFormMixin,
    EveryEngageMixin,
    EveryPageMixin,
)


class EveryCreateViewMixin(
    EveryThingMixin, EveryGetObjectMixin, EveryEditMixin, CreateView
):
    pass


class EveryUpdateViewMixin(
    EveryThingMixin, EveryGetObjectMixin, EveryEditMixin, UpdateView
):
    pass


class EveryDeleteViewMixin(
    EveryThingMixin, EveryGetObjectMixin, EveryDeleteMixin, DeleteView
):
    pass


# TODO: Consider ListView for Engage paginated
class EveryEngageViewMixin(
    EveryThingMixin,
    EveryGetObjectMixin,
    EveryEngageMixin,
    DetailView,
):
    pass


class EveryManyViewMixin(
    EveryThingMixin, EveryQuerySetMixin, EveryManyFormMixin, CreateView
):
    pass


class EveryOptimizeViewMixin(EveryThingMixin, TemplateView):
    pass


class EveryListViewMixin(EveryThingMixin, EveryQuerySetMixin, ListView):
    pass


class EveryPageViewMixin(EveryThingMixin, EveryPageMixin, TemplateView):
    pass


class EveryHomeViewMixin(EveryThingMixin, TemplateView):
    pass
