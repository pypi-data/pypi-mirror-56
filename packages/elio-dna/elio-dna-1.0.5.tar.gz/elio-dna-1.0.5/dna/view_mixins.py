# -*- encoding: utf-8 -*-
import copy
from django.apps import apps
from django.conf import settings
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from slugify.slugify import slugify
from dna.dna import DnaOfDjangoModel
from dna.forms import every_form
from dna.view_utils import (
    get_model_dna,
    get_page_dna,
    get_page_menu,
    get_page_name_from_slug,
    menu_lookahead,
)


class EveryThingMixin:
    _dna = None

    @property
    def site_dna(self):
        return copy.deepcopy(settings.SITE_DNA)

    @property
    def dna(self):
        if not self._dna:
            self._dna = DnaOfDjangoModel(
                settings.SCHEMA_PATH, self.site_dna, settings.DNA_DEPTH
            )
            self._dna.build()
        return self._dna

    @property
    def page_slug(self):
        return self.kwargs.get("page_slug", "")

    @property
    def page_name(self):
        return get_page_name_from_slug(
            self.site_dna, self.page_slug, self.thing_name
        )

    @property
    def thing_name(self):
        return self.kwargs.get("thing", "")

    @property
    def page_link(self):
        if self.page_name == self.thing_name:
            return reverse_lazy(
                "list.things",
                kwargs={"page_slug": self.page_slug, "thing": self.thing_name},
            )
        else:
            return reverse_lazy(
                "engage.page", kwargs={"page_slug": self.page_slug}
            )

    @property
    def page_menu(self):
        return get_page_menu(self.site_dna, self.page_name, self.dna.backbone)

    @property
    def Model(self):
        if self.thing_name:
            return apps.get_model(
                model_name=self.thing_name, app_label=settings.APP_NAME.lower()
            )
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_name"] = settings.APP_NAME.title()
        context["home_page"] = list(self.page_menu.get("page", {}))[0]
        context["page_name"] = self.page_name
        context["page_slug"] = self.page_slug
        context["thing_name"] = self.thing_name
        context["page_menu"] = self.page_menu
        return context


class EveryQuerySetMixin:

    paginate_by = 20

    def get_queryset(self):
        return self.Model.objects.all().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Don't extend the "page" querystring for standard lists.
        context["paginate_type"] = ""
        return context


class EveryGetObjectMixin:
    def get_object(self):
        obj = self.Model.objects.get(pk=self.kwargs.get("pk"))
        return obj


class EveryEditMixin:
    def get_form_class(self):
        role = self.kwargs.get("role", "")
        page_dna = get_page_dna(self.site_dna, self.page_name)
        model_dna = get_model_dna(page_dna, self.thing_name, role)
        elio_key = slugify(f"{self.page_name}-{self.thing_name}")
        field = model_dna.get("field", [])
        return every_form(
            self.Model, elio_key, self.page_link, model_dna.get("field", [])
        )


class EveryDeleteMixin:
    def get_success_url(self):
        return self.page_link


class EveryPageMixin:
    def get_template_names(self):
        """Decide whether to use the default template, or a customer template
        specified in the `SITE_DNA`."""
        custom_template = get_page_dna(self.site_dna, self.page_name).get(
            "template"
        )
        return custom_template or self.template_name

    def get_page_content(self, elio_type, default_template):
        """Build a content block.
        - An "engage" block is treated like a singleton for this page and types.
        - A "list" block handles a queryset for this page and types."""
        # Find out what schema will drive the content for this page.
        content = []
        page_dna = get_page_dna(self.site_dna, self.page_name).get(elio_type)
        # Does the SITE_DNA expect content of this elio_type?
        if page_dna:
            # For each thing type listed as set/dict/list.
            for thing_name in list(page_dna):
                elio_key = slugify(f"{self.page_name}-{thing_name}")
                # Get the model for this thing type.
                ContentThing = apps.get_model(
                    model_name=thing_name,  # settings.APP_NAME.title() + thing_name ,
                    app_label=settings.APP_NAME.lower(),
                )
                # Get the content as a singleton or queryset as per elio_type.
                if elio_type == "engage":
                    try:
                        # Get the record for this page and thing type.
                        content_thing = ContentThing.objects.get(
                            elio_key=elio_key,
                            elio_page=self.page_link,
                            elio_role=elio_type,
                        )
                    except ContentThing.DoesNotExist:
                        # Build a unique record for this page and thing type.
                        content_thing = ContentThing(
                            name=f"{self.page_name} {thing_name}",
                            elio_key=elio_key,
                            elio_page=self.page_link,
                            elio_role=elio_type,
                        )
                        content_thing.save()
                else:
                    content_thing = ContentThing.objects.filter(
                        elio_key=elio_key,
                        elio_page=self.page_link,
                        elio_role=elio_type,
                    ).order_by("name")
                # Build a dict for this content.
                thing_dna = {}
                if isinstance(page_dna, dict):
                    # The SITE_DNA may have settings like pagination or field.
                    thing_dna = page_dna.get(thing_name, {})
                thing_dna[elio_type] = content_thing
                thing_dna["thing_name"] = thing_name
                # Add a paginator if required.
                if thing_dna.get("paginate") and elio_type == "list":
                    paginator = Paginator(
                        content_thing, thing_dna.get("paginate")
                    )
                    thing_dna[elio_type] = paginator.get_page(
                        self.request.GET.get("page" + thing_name)
                    )
                    thing_dna["paginator"] = paginator
                    thing_dna["is_paginated"] = True
                    thing_dna["paginate_type"] = thing_name
                else:
                    thing_dna["paginator"] = None
                    thing_dna["is_paginated"] = False
                    thing_dna["paginate_type"] = ""
                # Always have a template.
                thing_dna["template"] = (
                    thing_dna.get("template") or default_template
                )
                # Append it to the content for this page and elio_type.
                content.append(thing_dna)
        return content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_engages"] = self.get_page_content(
            "engage", default_template="dna/_thing_engaged.html"
        )
        context["page_lists"] = self.get_page_content(
            "list", default_template="dna/_thing_listed.html"
        )
        return context
