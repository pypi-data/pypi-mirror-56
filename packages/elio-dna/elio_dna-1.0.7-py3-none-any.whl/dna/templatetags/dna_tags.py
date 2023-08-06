# -*- encoding: utf-8 -*-
from django import template
from dna.watermark import watermark


register = template.Library()


@register.simple_tag(name="thumbnail")
def thumbnail(image_path, dimensions):
    """Marshall call to the `watermark` method and return an easy_thumbnail."""
    thumb = watermark(image_path, dimensions)
    return thumb


@register.filter("has_no_merit")
def has_no_merit(value):
    """Determine if a field value has any merit at all."""
    if value:
        return not bool(str(value).strip())
    return (
        not value
        or value == "False"
        or value is None
        or value == "None"
        or str(value) == "0"
        or str(value) == "0.0"
    )


@register.filter("is_in")
def is_in(value, comma_list):
    """See if a value is in a comma separated list."""
    return value in comma_list.split(",")


# Development only.
@register.filter("dirt")
def dirt(value):
    """'Dish the dirt' on a template variable render the output of `dir`."""
    return dir(value)


@register.filter("flip_boo")
def flip_boo(value):
    """Flip a boolean value from True to False and back."""
    return bool(not value)


# need to add 'django.core.context_processors.request' to settings.TEMPLATES
@register.simple_tag(takes_context=True)
def qrystr_in_concert(context, name, value):
    """Replace a querystring parameter in concert with existing querystrings."""
    request = context["request"]
    dict_ = request.GET.copy()
    dict_[name] = value
    return dict_.urlencode()
