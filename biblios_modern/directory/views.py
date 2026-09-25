from django.views.generic import DetailView, ListView, TemplateView

from .filters import LibraryFilter
from .forms import SearchForm
from .models import Home, Library


class HomeView(TemplateView):
    """Odpowiednik starego views.home. Zamiast wycofanego render_to_response
    (usuniętego w Django 3.0) używa standardowego TemplateView."""

    template_name = "directory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["home_entries"] = Home.objects.all()
        return context


class LibraryListView(ListView):
    """
    Odpowiednik starej funkcji `index`.

    Różnice względem oryginału:
    - Stary kod budował DWIE oddzielne listy z bazy (queryset_list do
      wyszukiwania `q` i osobno library_list do filtra `LFilter`), a potem
      paginował tylko tę pierwszą - filtr (status/typ/sieć/województwo) i
      wyszukiwarka faktycznie się ze sobą nie łączyły. Tutaj `q` i filtr
      działają razem na jednym, wspólnym querysecie.
    - Paginacja przez wbudowany mechanizm ListView (paginate_by) zamiast
      ręcznego Paginatora w widoku.
    - `.only()` ogranicza pobierane kolumny do tych faktycznie użytych na
      liście wyników - mniej danych z bazy przy dużych katalogach.
    """

    model = Library
    template_name = "directory/list.html"
    context_object_name = "libraries"
    paginate_by = 20

    def get_queryset(self):
        queryset = Library.objects.all().only(
            "name", "slug", "type", "chain", "state", "city", "street", "url", "status"
        )
        query = self.request.GET.get("q", "")
        if query:
            queryset = queryset.search(query)
        self.filterset = LibraryFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        context["search_form"] = SearchForm(self.request.GET or None)
        context["query"] = self.request.GET.get("q", "")
        return context

    def get_template_names(self):
        # Zapytania wysłane przez htmx (patrz forms.py: hx-get/hx-trigger)
        # dostają tylko fragment z listą wyników + paginacją, bez całej
        # strony wokół - to daje "wyszukiwanie na żywo" bez pisania
        # własnego JS i bez przenoszenia stanu filtrów do JS-owego stanu.
        if self.request.headers.get("HX-Request") == "true":
            return ["directory/_results.html"]
        return [self.template_name]


class LibraryDetailView(DetailView):
    """Odpowiednik starego views.entity - teraz po `slug` (ładniejsze,
    czytelne URL-e) zamiast po numerycznym `library_id`, z fallbackiem
    404 obsługiwanym automatycznie przez get_object_or_404 wewnątrz DetailView."""

    model = Library
    template_name = "directory/detail.html"
    context_object_name = "library"
