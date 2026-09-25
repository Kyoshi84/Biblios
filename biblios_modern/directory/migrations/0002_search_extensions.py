from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):
    """
    Włącza rozszerzenia PostgreSQL potrzebne do wyszukiwarki
    (directory/managers.py):
    - pg_trgm: podobieństwo trigramowe (TrigramSimilarity) - pozwala
      znaleźć "Biblioeka Miejska" mimo literówki.
    - unaccent: pozwala docelowo dopisać wyszukiwanie ignorujące polskie
      znaki diakrytyczne (np. "Lodz" trafia też w "Łódź").

    Wymaga uprawnień superusera bazy przy pierwszym uruchomieniu migracji
    (CREATE EXTENSION). Na SQLite ta migracja jest pomijana - patrz
    fallback `_fallback_search` w managers.py.
    """

    dependencies = [("directory", "0001_initial")]

    operations = [
        TrigramExtension(),
        UnaccentExtension(),
    ]
