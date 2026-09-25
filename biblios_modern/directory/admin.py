from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Home, Library
from .resources import LibraryResource


@admin.register(Library)
class LibraryAdmin(ImportExportModelAdmin):
    """
    Różnice względem oryginalnego LibraryAdmin:
    - Metoda `name(self, obj): return obj.library.name` została usunięta -
      w oryginale przesłaniała pole modelu o tej samej nazwie (`name` jest
      polem Library, nie relacją do innego obiektu `library`) i w
      praktyce nigdy by się nie wykonała / była pozostałością po innej,
      wcześniejszej wersji modelu z osobnym Adress.
      Dwie linijki `name.admin_order_field = ...` i
      `name.short_description = ...` były zresztą źle wcięte (mieszanka
      tabów i spacji) - to sam w sobie błąd składni w Pythonie 3.
    - `export_to_csv` (Python 2, niejawny import) zastąpione przez
      ImportExportModelAdmin z django-import-export - patrz resources.py.
    - list_editable pozwala zmienić status prosto z listy, bez wchodzenia
      w szczegóły rekordu.
    """

    resource_classes = [LibraryResource]
    list_display = ["name", "type", "city", "state", "status", "published"]
    list_display_links = ["name"]
    list_editable = ["status"]
    list_filter = ["status", "type", "chain", "state", "city"]
    search_fields = ["name", "owner", "siglum", "email", "city", "street"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 50


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_display_links = ["title"]
    search_fields = ["title", "content"]
