# -*- encoding: utf-8 -*-
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from dna.view_mixins import (
    EveryThingMixin,
    EveryQuerySetMixin,
    EveryGetObjectMixin,
    EveryEditMixin,
    EveryPageMixin,
    EveryDeleteMixin,
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
    EveryThingMixin,
    EveryGetObjectMixin,
    EveryQuerySetMixin,
    EveryDeleteMixin,
    DeleteView,
):
    pass


class EveryEngageViewMixin(
    EveryThingMixin, EveryQuerySetMixin, EveryGetObjectMixin, DetailView
):
    pass


class EveryIterateViewMixin(EveryThingMixin, TemplateView):
    pass


class EveryOptimizeViewMixin(EveryThingMixin, TemplateView):
    pass


class EveryListViewMixin(EveryThingMixin, EveryQuerySetMixin, ListView):
    pass


class EveryPageViewMixin(EveryThingMixin, EveryPageMixin, TemplateView):
    pass


class EveryHomeViewMixin(EveryThingMixin, TemplateView):
    pass
