from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import LibraryQuerySet


class Library(models.Model):
    """
    Uwagi do migracji ze starego modelu:
    - _unicode_ / _str_ w oryginale to literówka - w Pythonie metody specjalne
      wymagają PODWÓJNEGO podkreślenia (__str__). Stary kod nigdy faktycznie
      nie nadpisywał wyświetlanej nazwy obiektu (w adminie/shellu i tak
      pokazywało się "Library object").
    - Cztery osobne krotki *_CHOICES z literówką "Pbliczna" (Publiczna)
      zamienione na django.db.models.TextChoices - jedno miejsce prawdy,
      bez duplikowania tych samych wartości w settings.py.
    - Usunięto model Adress/FK do Library - w bieżącym kodzie repo model
      Adress w ogóle nie istniał w models.py (tylko w starej migracji
      0001 i w search_indexes.py, który przez to nie dało się w ogóle
      zaimportować). Adres mieszka bezpośrednio w Library, tak jak
      faktycznie było używane.
    - Dodano indeksy bazodanowe na polach używanych do wyszukiwania/filtrowania.
    - published: auto_now_add zamiast wymaganego ręcznie pola bez wartości
      domyślnej (w adminie dało się dodać rekord z pustą datą i wywalało 500).
    """

    class LibraryType(models.TextChoices):
        PUBLIC = "P", _("Publiczna")
        ACADEMIC = "N", _("Naukowa")

    class Chain(models.TextChoices):
        PUBLIC = "P", _("Publiczna")
        ACADEMIC = "N", _("Naukowa")

    class Status(models.TextChoices):
        INACTIVE = "N", _("Nieaktywny")
        ACTIVE = "A", _("Aktywny")

    class Voivodeship(models.TextChoices):
        DOLNOSLASKIE = "0", _("Dolnośląskie")
        KUJAWSKO_POMORSKIE = "1", _("Kujawsko-pomorskie")
        LUBELSKIE = "2", _("Lubelskie")
        LUBUSKIE = "3", _("Lubuskie")
        LODZKIE = "4", _("Łódzkie")
        MALOPOLSKIE = "5", _("Małopolskie")
        MAZOWIECKIE = "6", _("Mazowieckie")
        OPOLSKIE = "7", _("Opolskie")
        PODKARPACKIE = "8", _("Podkarpackie")
        PODLASKIE = "9", _("Podlaskie")
        POMORSKIE = "10", _("Pomorskie")
        SLASKIE = "11", _("Śląskie")
        SWIETOKRZYSKIE = "12", _("Świętokrzyskie")
        WARMINSKO_MAZURSKIE = "13", _("Warmińsko-mazurskie")
        WIELKOPOLSKIE = "14", _("Wielkopolskie")
        ZACHODNIOPOMORSKIE = "15", _("Zachodniopomorskie")

    name = models.CharField("Nazwa instytucji", max_length=200, db_index=True)
    phone = PhoneNumberField("Telefon", blank=True)
    published = models.DateTimeField("Data wprowadzenia", auto_now_add=True)
    url = models.URLField("Strona internetowa", max_length=255, blank=True)
    email = models.EmailField("Email", max_length=254, blank=True)
    type = models.CharField("Typ biblioteki", max_length=1, choices=LibraryType.choices)
    chain = models.CharField("Sieć bibliotek", max_length=1, choices=Chain.choices)
    owner = models.CharField("Organizator", max_length=100, db_index=True)
    siglum = models.CharField("Siglum", max_length=15, blank=True)
    notes = models.TextField("Uwagi", blank=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    street = models.CharField("Ulica", max_length=128, blank=True)
    zip_code = models.CharField("Kod pocztowy", max_length=6, blank=True)
    city = models.CharField("Miasto", max_length=50, db_index=True)
    state = models.CharField("Województwo", max_length=2, choices=Voivodeship.choices)
    status = models.CharField("Status", max_length=1, choices=Status.choices, default=Status.ACTIVE)

    objects = LibraryQuerySet.as_manager()

    class Meta:
        verbose_name = "Biblioteka"
        verbose_name_plural = "Biblioteki"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["status", "city"]),
            models.Index(fields=["type", "chain", "state"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:200]
            slug = base_slug
            n = 1
            while Library.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base_slug}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("directory:detail", kwargs={"slug": self.slug})


class Home(models.Model):
    title = models.CharField("Tytuł", max_length=100)
    content = models.TextField("Zawartość", max_length=1000)

    class Meta:
        verbose_name = "Strona startowa"
        verbose_name_plural = "Strona startowa"

    def __str__(self):
        return self.title
