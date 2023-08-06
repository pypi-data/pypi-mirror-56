from easy_thumbnails.conf import Settings as easy_thumbnails_defaults

THUMBNAIL_WATERMARK = {
    "logo": {"name": "static/apple-touch-icon.png", "opacity": 0.7}
}

THUMBNAIL_PROCESSORS = easy_thumbnails_defaults.THUMBNAIL_PROCESSORS

THUMBNAIL_DEFAULT_OPTIONS = {"size": (100, 100), "crop": "center"}

THUMBNAIL_ALIASES = {
    "": {
        "960x720": {
            "size": (960, 720),
            "crop": False,
            "autocrop": True,
            "background": "white",
            "watermark": "logo",
            "upscale": True,
        },
        "640x480": {
            "size": (640, 480),
            "crop": False,
            "autocrop": True,
            "background": "white",
            "watermark": "logo",
            "upscale": True,
        },
        "300x300": {
            "size": (300, 300),
            "crop": "center",
            "autocrop": True,
            "background": "white",
            "watermark": "logo",
            "upscale": True,
        },
        "100x100": THUMBNAIL_DEFAULT_OPTIONS,
    }
}

DNA_BASE_MODEL_NAME = "Thing"
DNA_ENUMERATION_MODEL_NAME = "Enumeration"

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

# Because lowercase field names clash with propername Model names!
SILENCED_SYSTEM_CHECKS = [
    "models.E006"
]  # Or add "Model" to the name of each model. Or django-polymorphic?


SCHEMA_VERSION = "3.9"
SCHEMA_PATH = f"schemaorg/data/releases/{SCHEMA_VERSION}/all-layers.jsonld"
