from import_export import resources

from .models import Library


class LibraryResource(resources.ModelResource):
    """Zastępuje ręcznie pisany actions.py (import `from actions import
    export_to_csv` był niejawnym importem względnym w stylu Python 2 -
    w Python 3 rzuca ImportError) oraz zależność `unicodecsv` (pakiet
    istniał wyłącznie po to, by obejść to, że csv w Pythonie 2 nie radził
    sobie z Unicode - w Pythonie 3 wbudowany moduł csv robi to natywnie,
    więc unicodecsv jest zbędny).

    django-import-export daje od razu eksport/import CSV, XLS i XLSX
    (README wymieniał wszystkie trzy formaty) prosto z panelu admina, z
    podglądem różnic przed zatwierdzeniem importu.
    """

    class Meta:
        model = Library
        fields = (
            "id",
            "name",
            "type",
            "chain",
            "owner",
            "siglum",
            "phone",
            "email",
            "url",
            "street",
            "zip_code",
            "city",
            "state",
            "status",
            "published",
        )
        export_order = fields
