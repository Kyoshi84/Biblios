# Biblios — zmodernizowana wersja (Python 3.12+ / Django 5.2 LTS)

Ten katalog to uwspółcześniona wersja oryginalnej aplikacji z `contacts/biblios`
(książka adresowa bibliotek, Django 1.9/1.10, 2016/2017). Stary kod pozostaje
w repozytorium bez zmian (`biblios/`, `contacts/`) — dla porównania i jako
punkt odniesienia przy migracji ewentualnych danych.

## Co zostało zmienione i dlaczego

### Wersje i konfiguracja
- **Django 1.9/1.10 → Django 5.2 LTS** (wsparcie bezpieczeństwa do 04/2028),
  **Python 2/3 → Python 3.12+**.
- `MIDDLEWARE_CLASSES` → `MIDDLEWARE`; usunięto
  `SessionAuthenticationMiddleware` (nie istnieje od Django 1.10 — w starym
  kodzie i tak nic nie robił, tylko czekał, aż ktoś odpali projekt na
  nowszej wersji Django i dostanie `ImproperlyConfigured`).
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, dane bazy danych — teraz czytane
  ze zmiennych środowiskowych (`django-environ`, plik `.env`, patrz
  `.env.example`), a nie zapisane na sztywno w repo.
- Naprawiono literówkę `LANGUAGE_CODE = 'PL'` → `'pl'`, usunięto wycofane
  `USE_L10N`, dodano `DEFAULT_AUTO_FIELD`.
- `TEMPLATES['DIRS']` budowane z `BASE_DIR`, a nie zahardkodowane
  `/Biblios/contacts/biblios/templates` (działało tylko na jednej maszynie).
- Poprawiono realny błąd: `apps.py` miał `name = 'libraries'`, podczas gdy
  katalog i `INSTALLED_APPS` używały `biblios` — przy starcie na nowszym
  Django kończyłoby się to błędem konfiguracji.
- `from actions import export_to_csv` (niejawny import relatywny, składnia
  Python 2) — w Python 3 rzuca `ImportError`. Zastąpione przez
  `django-import-export` (patrz niżej).
- `_unicode_` / `_str_` (literówka — metody specjalne wymagają **podwójnego**
  podkreślenia: `__str__`) → poprawne `__str__`.

### Zależności
| Stare (nieaktualne/nierozwijane) | Nowe |
|---|---|
| `django-haystack` (`SimpleEngine`) | własny `LibraryQuerySet.search()` — Postgres FTS + trigramy |
| `django-redactor` (brak wsparcia dla Django ≥ 3 od 2019) | zwykłe `TextField` (opcjonalnie `django-ckeditor-5`) |
| `unicodecsv` (obejście dla Python 2) | wbudowany `csv`, poprzez `django-import-export` |
| ręczny `actions.py` (eksport CSV) | `django-import-export` — CSV **i** XLS/XLSX z panelu admina, tak jak było w README |

### Model i dane
- `Library.STATUS/TYPE/CHAIN/STATE_CHOICES` — z krotek (zduplikowanych też w
  `settings.py`) na `models.TextChoices`, jedno źródło prawdy.
- Poprawiono literówkę „Pbliczna” → „Publiczna”.
- Dodano `db_index=True` i `Meta.indexes` na polach używanych do
  wyszukiwania/filtrowania (`name`, `owner`, `city`, `(status, city)`,
  `(type, chain, state)`).
- `slug` generowany automatycznie i gwarantowany unikalny (`save()`),
  zamiast pustego pola, które trzeba było ręcznie wypełniać w adminie.
- Usunięto martwy model `Adress` — w bieżącym kodzie repo istniał tylko w
  starej migracji i w (i tak zepsutym) `search_indexes.py`; adres od dawna
  mieszkał bezpośrednio w `Library`.

### Wyszukiwarka — najważniejsza zmiana
Stary `django-haystack` z `HAYSTACK_CONNECTIONS = {'ENGINE': 'SimpleEngine'}`
**nie buduje żadnego prawdziwego indeksu** — przy każdym zapytaniu ładuje
wszystkie rekordy do pamięci Pythona i robi liniowe porównanie podciągów.
W praktyce to dokładnie to samo, co stary ręczny `Q(...icontains...)` w
`views.py`, tylko z dodatkową, nierozwijaną od lat zależnością i osobnym
plikiem szablonu indeksu, który nie dawał się nawet zaimportować
(`search_indexes.py` importował nieistniejący model `Adress`).

Nowe rozwiązanie (`directory/managers.py`, `Library.objects.search(q)`):

1. **PostgreSQL (zalecane, produkcja)** — pełnotekstowe wyszukiwanie
   (`SearchVector`/`SearchRank`, konfiguracja językowa `polish`) z wagami
   pól (nazwa > miasto/organizator/siglum > ulica/notatki), połączone z
   `TrigramSimilarity` (rozszerzenie `pg_trgm`) jako uzupełnieniem — dzięki
   temu literówka w zapytaniu („Bibliteka” zamiast „Biblioteka”) albo inna
   forma fleksyjna („bibliotece”) nadal trafia w wynik. Migracja
   `0002_search_extensions.py` włącza `pg_trgm` i `unaccent` (to drugie
   pod przyszłe wyszukiwanie ignorujące polskie znaki diakrytyczne, np.
   „Lodz” → „Łódź”).
2. **SQLite / inne bazy (dev)** — automatyczny fallback na `icontains` po
   tych samych polach, żeby projekt dało się odpalić bez Postgresa.
3. Wyszukiwanie tekstowe (`q`) i filtrowanie (`django-filter`: status, typ,
   sieć, województwo) **działają teraz razem** na jednym querysecie — w
   oryginale `index()` budował dwa niezależne querysety i faktycznie się
   nie łączyły.
4. **UX**: pole wyszukiwania podpięte pod htmx (`hx-get`/`hx-trigger`) —
   wyniki odświeżają się przy pisaniu (300 ms debounce) bez przeładowania
   całej strony, bez pisania własnego JS.

**Dalsze usprawnienia do rozważenia w miarę wzrostu bazy** (nieobjęte tym
PR-em, bo dla kilkuset–kilku tysięcy rekordów Postgres FTS + trigramy w
zupełności wystarczą):
- `unaccent` w samym zapytaniu wyszukiwania (nie tylko w migracji) — pełne
  ignorowanie polskich znaków diakrytycznych.
- Podpowiedzi „czy chodziło Ci o…” przy zerowych wynikach (na bazie
  `TrigramSimilarity` już mamy dane do tego).
- Przy naprawdę dużym wolumenie (dziesiątki–setki tysięcy rekordów) lub
  potrzebie wyszukiwania wielojęzycznego z zaawansowanym rankingiem —
  wydzielony silnik (Meilisearch/Typesense przez `django-meilisearch`/REST,
  albo Elasticsearch przez `django-elasticsearch-dsl`).

### Widoki, adres URL, admin
- Funkcje `index`/`entity` → klasowe `LibraryListView`/`LibraryDetailView`
  (`ListView`/`DetailView`), paginacja przez wbudowany `paginate_by`.
- Adresy po `slug` (`/biblioteki/<slug>/`) zamiast numerycznego ID.
- `render_to_response` (usunięte w Django 3.0) → `TemplateView`.
- `html_to_pdf_view` (odwoływał się do niezaimportowanego `HTML` z
  weasyprint i miał kod za `return`, więc nigdy nie działał) — usunięty;
  eksport do PDF/CSV/XLS/XLSX jest teraz w panelu admina przez
  `django-import-export`.
- Statyczny formularz kontaktowy bez żadnej logiki backendowej (w oryginale
  `<form>` bez `action`/widoku obsługującego POST) — usunięty jako
  niefunkcjonalny; do ewentualnego dodania później jako prawdziwy
  `forms.Form` + wysyłka e-mail.
- Panel admina: `django-import-export`, poprawiony (usunięty, bo był
  błędny i przesłaniał pole modelu) `LibraryAdmin.name()`, `list_editable`
  dla statusu, więcej filtrów.
- Szablony: Bootstrap 3.3.7 → Bootstrap 5, poprawiony `{% load staticfiles %}`
  (tag usunięty w Django 3.1) → `{% load static %}`.

## Uruchomienie lokalnie

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # i uzupełnij wartości
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Bez Postgresa: w `.env` ustaw `DATABASE_URL=sqlite:///db.sqlite3` —
projekt wystartuje, wyszukiwarka przełączy się automatycznie na tryb
`icontains` (patrz `directory/managers.py`).

## Automatyczne wdrażanie (CI/CD) na Render.com

Repozytorium zawiera `render.yaml` (tzw. Blueprint) w tym katalogu. Dzięki
niemu Render sam tworzy i konfiguruje usługi opisane w tym pliku — nie
trzeba pisać osobnego workflow w GitHub Actions ani logować się po SSH.

**Jednorazowa konfiguracja:**
1. Załóż konto na [render.com](https://render.com) (logowanie przez GitHub).
2. „New +” → „Blueprint” → wskaż repozytorium `Kyoshi84/Biblios`. Render
   sam znajdzie `biblios_modern/render.yaml`.
3. Zatwierdź — Render utworzy usługę web (`biblios`) oraz bazę PostgreSQL
   (`biblios-db`) i połączy je automatycznie przez `DATABASE_URL`.
4. Pierwszy deploy potrwa kilka minut (instalacja zależności, `collectstatic`,
   `migrate`). Potem aplikacja jest dostępna pod `https://biblios.onrender.com`
   (albo pod docelową domeną, jeśli ją podepniesz w panelu Render).

**Od tej pory automatyzacja jest pełna:** każdy push na gałąź `main` —
również taki, który wykonuje tu Claude przez integrację z GitHub —
automatycznie uruchamia build i deploy (`autoDeploy: true` w `render.yaml`).
Nie trzeba nic więcej klikać ani konfigurować.

**Uwagi:**
- Darmowy plan usypia serwis po ~15 minutach bez ruchu (pierwsze żądanie po
  przerwie budzi go z opóźnieniem rzędu kilkunastu sekund) i darmowa baza
  wygasa po 90 dniach — wystarczające na start/demo, do produkcji warto
  przejść na płatny plan (Starter, ok. $7/mies. za web + $6/mies. za bazę).
- Superusera do panelu admina tworzy się jednorazowo przez zakładkę
  „Shell” w panelu Render: `python manage.py createsuperuser`.
- Jeśli wolisz własny VPS zamiast PaaS (pełna kontrola, bez usypiania) —
  to też da się zautomatyzować, przez GitHub Actions + SSH/rsync +
  systemd + Nginx; daj znać, przygotuję taki workflow jako alternatywę.

## Migracja danych ze starej wersji

Stare dane (SQLite z `contacts/db.sqlite3`, jeśli istnieją) można
przenieść przez `dumpdata`/`loaddata` ze starego projektu do nowego —
nazwy pól modelu `Library` zostały zachowane 1:1, więc wystarczy
zmapować `app_label` (`biblios` → `directory`) w wyeksportowanym JSON
przed `loaddata`.
