# -*- encoding: utf-8 -*-
import copy
from django.db import transaction
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from slugify.slugify import slugify
from dna.crispr import Crispr
from dna.dna import DnaOfDjangoModel
from dna.forms import every_form
from dna.models import eliomany_model, EveryModel
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
    def elio_key(self):
        return slugify(f"{self.page_name}-{self.thing_name}")

    @property
    def page_menu(self):
        return get_page_menu(self.site_dna, self.page_name, self.dna.backbone)

    @property
    def Model(self):
        if self.thing_name:
            return EveryModel(self.thing_name)
        return None

    @property
    def ElioMany(self):
        return EveryModel("ElioMany")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_name"] = settings.APP_NAME.title()
        context["home_page"] = list(self.page_menu.get("page", {}))[0]
        context["page_name"] = self.page_name
        context["page_slug"] = self.page_slug
        context["thing_name"] = self.thing_name
        context["page_menu"] = self.page_menu
        return context


class EveryManyFormMixin:
    _many_thing = ""

    @property
    def parent(self):
        return self.kwargs.get("pk", "")

    @property
    def prop_name(self):
        return self.kwargs.get("prop", "")

    @property
    def many_thing(self):
        if not self._many_thing:
            prop = self.dna.crispr.property_of_by_name(self.prop_name)
            all_types_of = Crispr.property_types_of(prop, self.dna.domain)
            primitive_types_of = self.dna.crispr.primitive_types_of(
                all_types_of
            )
            class_types_of = set(all_types_of).difference(
                set(primitive_types_of)
            )
            if not class_types_of:
                class_types_of = set([f"{self.dna.domain}/Thing"])
            self._many_thing = self.dna.crispr.name_from_url(
                list(class_types_of)[0]
            )
        return self._many_thing

    @property
    def FieldModel(self):
        return EveryModel(self.many_thing)

    def get_form_class(self):
        return every_form(self.FieldModel, self.elio_key, self.page_link)

    def form_valid(self, form):
        parent = self.get_object()
        with transaction.atomic():
            self.object = form.save()
            many = self.ElioMany(
                many_engaged=parent,
                many_listed=self.object,
                engaged_thing=self.thing_name,
                listed_field=self.prop_name,
                listed_thing=self.many_thing,
                elio_key=self.elio_key,
                elio_page=self.page_link,
                elio_role="many",
            )
            many.save()
        return HttpResponseRedirect(parent.get_host_page())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["many_thing"] = self.many_thing
        context["prop_name"] = self.prop_name
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
        field = model_dna.get("field", [])
        return every_form(
            self.Model,
            self.elio_key,
            self.page_link,
            model_dna.get("field", []),
        )

    def form_invalid(self, form):
        print("form_invalid!", form)
        return super().form_invalid(form)


class EveryDeleteMixin:
    def get_success_url(self):
        return self.page_link


class ManyMixin:
    def _many(self, content_thing, elio_key, listed_field):
        """The many2many relationships for an engaged content's `many` field."""
        return self.ElioMany.objects.filter(
            many_engaged=content_thing,
            listed_field=listed_field,
            elio_key=elio_key,
            elio_page=self.page_link,
            elio_role="many",
        ).order_by("many_listed__name")


class EveryEngageMixin(ManyMixin):

    # TODO: Consider a ListView for engage things paginated.
    # paginate_by = 1
    # def get_queryset(self):
    #     return self.Model.objects.filter(
    #         elio_key=self.elio_key,
    #         elio_page=self.page_link,
    #     ).order_by("name")

    def get_many(self):
        content = {}
        page_dna = get_page_dna(self.site_dna, self.page_name).get("list", {})
        many_fields = page_dna.get(self.thing_name, {}).get("many", {})
        for listed_field in many_fields:
            content[listed_field] = self._many(
                self.get_object(), self.elio_key, listed_field
            )
        return content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Don't extend the "page" querystring for standard lists.
        context["many"] = self.get_many()
        return context


class EveryPageMixin(ManyMixin):
    def _engagement(self, thing_dna, ContentThing):
        thing_name = thing_dna["thing_name"]
        try:
            # Get the record for this page and thing type.
            content_thing = ContentThing.objects.get(
                elio_key=thing_dna["elio_key"],
                elio_page=self.page_link,
                elio_role="engage",
            )
        except ContentThing.DoesNotExist:
            # Build a unique record for this page and thing type.
            content_thing = ContentThing(
                name=f"{self.page_name} {thing_name}",
                elio_key=thing_dna["elio_key"],
                elio_page=self.page_link,
                elio_role="engage",
            )
            content_thing.save()
        thing_dna["engage"] = content_thing
        # Handle any `many` field
        many_dna = {}
        for listed_field in thing_dna.get("many", []):
            many_dna[listed_field] = self._many(
                content_thing, thing_dna["elio_key"], listed_field
            )
        thing_dna["many"] = many_dna
        return thing_dna

    def _listing(self, thing_dna, ContentThing):
        thing_name = thing_dna["thing_name"]
        content_thing = ContentThing.objects.filter(
            elio_key=thing_dna["elio_key"],
            elio_page=self.page_link,
            elio_role="list",
        ).order_by("name")
        # Add a paginator if required.
        if thing_dna.get("paginate"):
            paginator = Paginator(content_thing, thing_dna.get("paginate"))
            thing_dna["list"] = paginator.get_page(
                self.request.GET.get("page" + thing_name)
            )
            thing_dna["paginator"] = paginator
            thing_dna["is_paginated"] = True
            thing_dna["paginate_type"] = thing_name
        else:
            thing_dna["list"] = content_thing
            thing_dna["paginator"] = None
            thing_dna["is_paginated"] = False
            thing_dna["paginate_type"] = ""
        return thing_dna

    def get_template_names(self):
        """Decide whether to use the default template, or a customer template
        specified in the `SITE_DNA` for this page."""
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
                # Get the model for this thing type.
                ContentThing = EveryModel(thing_name)
                # Build a dict for this content.
                thing_dna = {}
                if isinstance(page_dna, dict):
                    # The SITE_DNA may have settings like pagination or field.
                    thing_dna = page_dna.get(thing_name, {})
                thing_dna["elio_key"] = slugify(
                    f"{self.page_name}-{thing_name}"
                )
                thing_dna["thing_name"] = thing_name

                # Get the content as a singleton or queryset as per elio_type.
                if elio_type == "engage":
                    thing_dna = self._engagement(thing_dna, ContentThing)

                elif elio_type == "list":
                    thing_dna = self._listing(thing_dna, ContentThing)

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
