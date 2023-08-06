import os
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer


self_dir = os.path.dirname(os.path.realpath(__file__))
app_path = os.sep.join(self_dir.split(os.sep)[:-1])


def watermark(thing_image, dimension):
    thumbnail_options = settings.THUMBNAIL_ALIASES[""][dimension]
    thumber = get_thumbnailer(thing_image)
    thumb = thumber.get_thumbnail(thumbnail_options)
    return thumb.url
