"""Django-Einstellungen für Tests."""

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-test-key-not-for-production"  # noqa: S105

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_htmx",
    "insight_ui",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "core.context_processor.project_context",
            ]
        },
    }
]

ASGI_APPLICATION = "core.asgi.application"

# Database
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}}

# Internationalization
LANGUAGE_CODE = "de-de"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Internationalization
LANGUAGES = [
    ("de", "Deutsch"),
    ("en", "English"),
    ("es", "Español"),
    ("fr", "Français"),
    ("ar", "العربية"),
    ("zh", "中文"),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, "insight_ui", "locale")]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# WhiteNoise configuration
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Env-Variables
PROJECT_NAME = "Insight UI"
PROJECT_DESCRIPTION = "Our base template to build Web UI's for our applications"
PROJECT_AUTHOR = "Alpin Insight AI"
VERSION = "0.1.0"

# Insight UI Einstellungen
INSIGHT_UI = {
    "theme": "light",
    "favicon": "insight_ui/favicon/favicon.ico",
    "favicon_32": "insight_ui/favicon/favicon-32x32.png",
    "favicon_16": "insight_ui/favicon/favicon-16x16.png",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/logo.svg",
    "msapplication_TileColor": "#da532c",
    "theme_color": "#ffffff",
    "branding": {"name": PROJECT_NAME, "logo": None},
    "meta": {
        "seo": {
            "description": PROJECT_DESCRIPTION,
            "keywords": "Django, Insight UI, base template",
            "author": PROJECT_AUTHOR,
        },
        "open_graph": {
            "title": PROJECT_NAME,
            "description": PROJECT_DESCRIPTION,
            "site_name": "Django Insight UI",
            "url": "",
        },
        "twitter": {
            "title": PROJECT_NAME,
            "description": PROJECT_DESCRIPTION,
            "site": "Django Insight UI",
            "author": PROJECT_AUTHOR,
        },
    },
}
