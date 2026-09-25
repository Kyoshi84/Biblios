"""
Wyszukiwarka katalogu.

Stary kod używał django-haystack z backendem 'simple_backend'
(HAYSTACK_CONNECTIONS -> SimpleEngine). SimpleEngine nie buduje żadnego
prawdziwego indeksu - przy każdym zapytaniu ładuje wszystkie rekordy do
pamięci i robi na nich zwykłe porównanie substringów w Pythonie. To znaczy,
że cały mechanizm haystack+search_indexes.py+szablon
search/indexes/biblios/library_text.txt nie dawał tu ŻADNEJ przewagi nad
prostym filter(icontains=...), a jedynie dokładał zależność (haystack nie był
aktualizowany od lat i nie deklaruje wsparcia dla Django >= 3) i osobny
plik indeksu do utrzymania. Dodatkowo search_indexes.py importował
nieistniejący już model `Adress` i się wywalał przy starcie.

Nowe podejście - jedna metoda `Library.objects.search(query)`:
- Na PostgreSQL: pełnotekstowe wyszukiwanie (SearchVector/SearchRank) +
  podobieństwo trigramowe (TrigramSimilarity) jako fallback, gdy zapytanie
  nie trafi we frazę dokładnie (literówki, odmiana przez przypadki:
  "biblioteka" vs "bibliotece"). Wagi pól (A/B) sprawiają, że trafienie w
  nazwę liczy się bardziej niż trafienie w notatki.
- Na innych bazach (np. SQLite w dev/testach) - zwykłe `icontains` po tych
  samych polach, żeby projekt dało się uruchomić bez Postgresa.

Wymagania produkcyjne (patrz README): rozszerzenie `pg_trgm` w PostgreSQL
oraz - opcjonalnie, dla wyszukiwania bez polskich znaków diakrytycznych -
rozszerzenie `unaccent`.
"""

from django.db import connection, models
from django.db.models import Q


class LibraryQuerySet(models.QuerySet):
    SEARCH_FIELDS = ["name", "owner", "city", "street", "siglum", "email", "notes"]

    def search(self, query):
        query = (query or "").strip()
        if not query:
            return self

        if connection.vendor == "postgresql":
            return self._postgres_search(query)
        return self._fallback_search(query)

    def _postgres_search(self, query):
        from django.contrib.postgres.search import (
            SearchQuery,
            SearchRank,
            SearchVector,
            TrigramSimilarity,
        )

        vector = (
            SearchVector("name", weight="A", config="polish")
            + SearchVector("owner", "city", "siglum", weight="B", config="polish")
            + SearchVector("street", "notes", weight="C", config="polish")
        )
        search_query = SearchQuery(query, config="polish")

        return (
            self.annotate(
                rank=SearchRank(vector, search_query),
                similarity=TrigramSimilarity("name", query),
            )
            .filter(Q(rank__gt=0.0) | Q(similarity__gt=0.15))
            .order_by("-rank", "-similarity", "name")
        )

    def _fallback_search(self, query):
        q = Q()
        for field in self.SEARCH_FIELDS:
            q |= Q(**{f"{field}__icontains": query})
        return self.filter(q).distinct()
