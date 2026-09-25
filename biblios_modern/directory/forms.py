from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(
        label="Szukaj",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nazwa, miasto, organizator, e-mail…",
                # hx-* atrybuty: włączają "live search" bez przeładowania strony
                # (patrz directory/templates/directory/list.html) - wymaga htmx,
                # które jest wczytywane z CDN w base.html. To opcjonalne
                # usprawnienie UX, cała logika i tak działa też bez JS.
                "hx-get": "",
                "hx-trigger": "keyup changed delay:300ms, search",
                "hx-target": "#results",
                "hx-push-url": "true",
            }
        ),
    )
