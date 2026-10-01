"""
Ustawienia projektu Biblios.

Zmiany względem starej wersji (Django 1.9/1.10):
- SECRET_KEY / DEBUG / ALLOWED_HOSTS / DATABASE_URL czytane ze zmiennych
  środowiskowych (django-environ), a nie zaszyte na sztywno w repo.
- MIDDLEWARE_CLASSES -> MIDDLEWARE (MIDDLEWARE_CLASSES nie istnieje od Django 1.10).
- Usunięto 'django.contrib.auth.middleware.SessionAuthenticationMiddleware'
  (usunięte z Django już w wersji 1.10 - w oryginale zostało po staremu i
  wywalałoby błąd przy starcie na nowszym Django).
- LANGUAGE_CODE poprawione na małe litery 'pl' (kody języków są wielkości liter
  wrażliwe; 'PL' w oryginalnym settings.py biblios/settings.py był błędny).
- USE_L10N usunięte - ustawienie zostało wycofane w Django 5.0 (zawsze True).
- DEFAULT_AUTO_FIELD ustawiony jawnie na BigAutoField (wymagane od Django 3.2+,
  inaczej Django przy każdym starcie zgłasza ostrzeżenie W042).
- TEMPLATES['DIRS'] budowane z BASE_DIR zamiast zahardkodowanej ścieżki
  '/Biblios/contacts/biblios/templates' (działało tylko na jednej konkretnej
  maszynie deweloperskiej).
- Usunięto 'haystack' (nieaktualizowany od lat, SimpleEngine i tak tylko robi
  liniowe porównania stringów w pamięci - patrz README, sekcja "Wyszukiwarka").
- Usunięto 'redactor' (django-redactor nie jest rozwijany od 2019 i nie
  deklaruje wsparcia dla Django >= 3). Pole 'notes' to teraz zwykłe
  TextField (opcjonalnie: django-ckeditor-5, patrz requirements.txt).
- Dodano django-import-export do obsługi CSV/XLS/XLSX (zastępuje ręczny,
  Python2-owy actions.py z pakietem unicodecsv).
- Dodano WhiteNoise do serwowania plików statycznych w produkcji.
- Dodano obsługę zmiennej RENDER_EXTERNAL_HOSTNAME, którą Render.com
  wstrzykuje automatycznie w środowisku produkcyjnym (patrz render.yaml)
  - dzięki temu nie trzeba ręcznie wpisywać domeny *.onrender.com do
  ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS po każdym deployu.
"""

import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DJANGO_DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

# Render.com wstawia tę zmienną automatycznie dla każdego serwisu web -
# https://render.com/docs/environment-variables - nie trzeba jej ustawiać
# ręcznie w panelu, wystarczy że render.yaml jest w repo (patrz niżej).
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_HOSTNAME}")

# Baza danych: PostgreSQL zalecany (pełnotekstowe wyszukiwanie + trigramy,
# patrz directory/managers.py i README). Działa też na SQLite (fallback na
# zwykłe `icontains`) - patrz DATABASE_URL w .env.example.
DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:///" + str(BASE_DIR / "db.sqlite3"))}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "django_filters",
    "phonenumber_field",
    "import_export",
    # projekt
    "directory",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]

# 'django.contrib.postgres' importuje psycopg już przy starcie aplikacji
# (nawet jeśli nic z niego jawnie nie importujemy) - włączamy je więc tylko
# gdy faktycznie jedziemy na PostgreSQL. Dzięki temu projekt da się też
# uruchomić lokalnie na SQLite bez instalowania psycopg (patrz
# directory/managers.py - fallback na zwykłe icontains, gdy wykryje inny
# wendor bazy).
if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    INSTALLED_APPS += ["django.contrib.postgres"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Baza danych: PostgreSQL zalecany (pełnotekstowe wyszukiwanie + trigramy,
# patrz directory/managers.py i README). Działa też na SQLite (fallback na
# zwykłe `icontains`) - patrz DATABASE_URL w .env.example.
DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:///" + str(BASE_DIR / "db.sqlite3"))}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pl"
TIME_ZONE = "Europe/Warsaw"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

PHONENUMBER_DB_FORMAT = "INTERNATIONAL"
PHONENUMBER_DEFAULT_REGION = "PL"

# Bezpieczeństwo produkcyjne - aktywne tylko gdy DEBUG=False.
if not DEBUG:
    # Render (i większość PaaS) terminuje SSL na swoim reverse proxy i do
    # aplikacji przekazuje już zwykłe HTTP - bez tego nagłówka
    # SECURE_SSL_REDIRECT wpadłby w nieskończoną pętlę przekierowań.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
