# -*- encoding: utf-8 -*-
from django import template
from dna.watermark import watermark


register = template.Library()


@register.simple_tag(name="thumbnail")
def thumbnail(image_path, dimensions):
    thumb = watermark(image_path, dimensions)
    return thumb


@register.filter("is_none_null_or_zero")
def is_none_null_or_zero(value):
    return not (
        not value
        or value == "False"
        or value is None
        or value == "None"
        or str(value) == "0"
        or str(value) == "0.0"
        or boolean(value.strip())
    )


@register.filter("is_in")
def is_in(value, comma_list):
    return value in comma_list.split(",")


@register.filter("dirt")
def dirt(value):
    return dir(value)


# need to add 'django.core.context_processors.request' to settings.TEMPLATES
# @register.simple_tag(takes_context=True)
# def url_replace(context, name, value):
#     request = context["request"]
#     dict_ = request.GET.copy()
#     dict_[name] = value
#     return dict_.urlencode()
