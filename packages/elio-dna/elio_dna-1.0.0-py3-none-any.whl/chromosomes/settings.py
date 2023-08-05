# -*- encoding: utf-8 -*-
import os
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATICFILES_DIRS = [os.path.join("chromosomes", "theme/dist")]

STATIC_ROOT = "chromosome_static"

STATIC_URL = "/static/"

MEDIA_ROOT = "chromosome_files"

MEDIA_URL = "/media/"

# Default App Settings
# Because lowercase field names clash with propername Model names!
SILENCED_SYSTEM_CHECKS = [
    "models.E006"
]  # Or add "Model" to the name of each model. Or django-polymorphic?
SITE_DNA = {"CreativeWork"}
DNA_DEPTH = 0
SCHEMA_VERSION = "3.9"
SCHEMA_PATH = f"schemaorg/data/releases/{SCHEMA_VERSION}/all-layers.jsonld"
ELIO_LIST = False


# Use CharField with these lengths for these properties.
DNA_SHORT_TEXT_FIELDS = {
    "name": 512,
    "disambiguatingDescription": 512,
    "gtin12": 12,
    "gtin13": 13,
    "gtin14": 14,
    "gtin8": 8,
    "naics": 6,
    "postalCode": 30,
    "flightNumber": 10,
    "branchCode": 10,
    "departureGate": 10,
    "arrivalGate": 10,
    "departureTerminal": 10,
    "arrivalTerminal": 10,
    "iataCode": 3,
    "icaoCode": 4,
    "departurePlatform": 10,
    "arrivalPlatform": 10,
    "busNumber": 10,
    "issn": 8,
    "isbn": 13,
    "isrcCode": 50,
    "iswcCode": 50,
    "vehicleIdentificationNumber": 17,
    "leiCode": 50,
    "courseCode": 50,
    "accessCode": 50,
}

# Use long text for these properties.
DNA_LONG_TEXT_FIELDS = (
    "articleBody",
    "awards",
    "benefits",
    "commentText",
    "dependencies",
    "description",
    "educationRequirements",
    "experienceRequirements",
    "incentives",
    "incentiveCompensation",
    "jobBenefits",
    "lodgingUnitDescription",
    "qualifications",
    "responsibilities",
    "reviewBody",
    "skills",
    "text",
    "transcript",
)
