from django.apps import AppConfig


class DirectoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # W starym kodzie name='libraries' nie zgadzało się z katalogiem/etykietą
    # aplikacji 'biblios' użytą w INSTALLED_APPS i include('libraries.urls') -
    # to realny błąd, który wywala Django przy starcie ("no installed app
    # with label ..."). Tutaj nazwa aplikacji jest spójna wszędzie.
    name = "directory"
    verbose_name = "Katalog bibliotek"
