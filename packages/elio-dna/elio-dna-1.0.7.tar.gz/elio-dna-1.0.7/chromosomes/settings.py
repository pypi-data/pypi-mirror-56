# -*- encoding: utf-8 -*-
import os
from dna.settings import *
from apep.env_var import get_env_variable, get_env_variable_bool

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "sx)8tn28l=e)wd^v#e!q6w2g3ige!bgskhm-sl%5grv==x$v=("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "livereload",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "easy_thumbnails",
    "dna",
    "chromosomes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "livereload.middleware.LiveReloadScript",
]

ROOT_URLCONF = "chromosomes.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "chromosomes.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "temp.db"}
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


APP_NAME = "chromosomes"

STATICFILES_DIRS = [os.path.join(APP_NAME, "theme/dist")]

STATIC_ROOT = "static"

STATIC_URL = "/elio_static/"

MEDIA_ROOT = "media"

MEDIA_URL = "/elio_media/"

# Default App Settings
# Because lowercase field names clash with propername Model names!
SILENCED_SYSTEM_CHECKS = [
    "models.E006"
]  # Or add "Model" to the name of each model. Or django-polymorphic?
WEB_PAGE_DNA = {
    "WebPage": {
        "field": [
            "image",
            "name",
            "alternateName",
            "disambiguatingDescription",
            "description",
            "text",
        ],
        "many": ["significantLinks"],
    }
}
DNA_DEPTH = 0
SITE_DNA = {
    "page": {
        APP_NAME.title(): {"engage": WEB_PAGE_DNA},
        "sep1": {"status": "spacer"},
        "Blog": {
            "engage": WEB_PAGE_DNA,
            "page": {
                "Bubbles": {
                    "list": {
                        "CreativeWork": {
                            "paginate": 5,
                            "template": "chromosomes/_list_bubble.html",
                            "field": [
                                "image",
                                "name",
                                "alternateName",
                                "disambiguatingDescription",
                                "description",
                                "text",
                            ],
                        }
                    }
                },
                "Articles": {
                    "list": {
                        "CreativeWork": {
                            "paginate": 10,
                            "field": [
                                "image",
                                "name",
                                "alternateName",
                                "description",
                                "text",
                                "creator",
                                "dateModified",
                                "datePublished",
                                "dateCreated",
                            ],
                            "many": ["comment"],
                        }
                    }
                },
            },
        },
        "Gallery": {
            "engage": WEB_PAGE_DNA,
            "list": {
                "Photograph": {
                    "paginate": 20,
                    "template": "chromosomes/_list_gallery.html",
                    "field": [
                        "name",
                        "alternateName",
                        "description",
                        "image",
                        "creator",
                        "dateCreated",
                    ],
                    "many": ["comment"],
                }
            },
        },
        "About": {
            "engage": {
                "AboutPage": {
                    "field": [
                        "name",
                        "alternateName",
                        "disambiguatingDescription",
                        "description",
                    ],
                    "many": ["reviews"],
                },
                "Organization": {
                    "title": "Contact",
                    "field": ["address", "founder"],
                    "many": ["email", "telephone", "founder"],
                },
            }
        },
        "Logout": {"url": "/"},
    }
}


SITE_DNA = {
    "page": {
        "Home": {
            "engage": {"WebPage": {"field": ["name", "description"]}},
            "list": {"Photograph": {"field": ["name", "image"]}},
        },
        "Blog": {
            "engage": {"WebPage": {
                "field": ["name", "description"],
                "many": ["image"]
                }
            },
            "list": {
                "WebPage": {"field": ["name", "description", "image"]}
            },
        },
        "About": {
            "engage": {
                "AboutPage": {"field": ["name", "description"]},
                "Organization": {
                    "field": ["name", "address", "telephone", "email"],
                    "many": ["contactPoints", "reviews"]
                },
            }
        },
        "Logout": {"url": "/"},
    }
}

SCHEMA_VERSION = "3.9"
SCHEMA_PATH = f"schemaorg/data/releases/{SCHEMA_VERSION}/all-layers.jsonld"
