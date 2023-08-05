# -*- encoding: utf-8 -*-
from django.conf import settings
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from dna.forms import every_form
from dna.views import (
    EveryViewMixin,
    EveryCreateViewMixin,
    EveryDeleteViewMixin,
    EveryDetailViewMixin,
    EveryListViewMixin,
    EveryUpdateViewMixin,
)


class ViewEveryThing(EveryViewMixin, TemplateView):
    template_name = "chromosomes/every_thing.html"


class ChromosomesCreateView(EveryCreateViewMixin):
    template_name = "chromosomes/thing_form.html"


class ChromosomesDeleteView(EveryDeleteViewMixin):
    template_name = "chromosomes/thing_delete.html"


class ChromosomesDetailView(EveryDetailViewMixin):
    template_name = "chromosomes/thing_detail.html"


class ChromosomesUpdateView(EveryUpdateViewMixin):
    template_name = "chromosomes/thing_form.html"


class ChromosomesListView(EveryListViewMixin):
    template_name = "chromosomes/thing_list.html"
