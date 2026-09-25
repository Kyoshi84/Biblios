import django_filters
from django import forms

from .models import Library


class LibraryFilter(django_filters.FilterSet):
    """
    Odpowiednik starego LFilter. Zmiany:
    - `name=CharFilter` usunięty - wyszukiwanie po nazwie i pozostałych
      polach tekstowych obsługuje teraz jedno pole `q` w SearchForm
      (patrz forms.py) podpięte pod Library.objects.search().
      Trzymanie dwóch równoległych mechanizmów wyszukiwania (osobno `q` w
      views.py i osobno `name` w filtrze) było mylące i niespójne w
      oryginalnym kodzie.
    - CheckboxSelectMultiple zamieniony na SelectMultiple ze stylem
      Bootstrap 5 (szablon), żeby długie listy (16 województw) nie zajmowały
      pół ekranu.
    """

    status = django_filters.MultipleChoiceFilter(
        choices=Library.Status.choices, widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )
    type = django_filters.MultipleChoiceFilter(
        choices=Library.LibraryType.choices, widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )
    chain = django_filters.MultipleChoiceFilter(
        choices=Library.Chain.choices, widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )
    state = django_filters.MultipleChoiceFilter(
        choices=Library.Voivodeship.choices, widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )

    class Meta:
        model = Library
        fields = ["status", "type", "chain", "state"]
