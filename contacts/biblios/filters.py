from django import forms
from django.conf import settings
from .models import Library
import django_filters


class LFilter(django_filters.FilterSet):
	status = django_filters.MultipleChoiceFilter(choices=Library.STATUS_CHOICES, widget=forms.CheckboxSelectMultiple)
	type = django_filters.MultipleChoiceFilter(choices=Library.TYPE_CHOICES, widget=forms.CheckboxSelectMultiple)
	chain = django_filters.MultipleChoiceFilter(choices=Library.CHAIN_CHOICES, widget=forms.CheckboxSelectMultiple)
	state = django_filters.MultipleChoiceFilter(choices=Library.STATE_CHOICES, widget=forms.CheckboxSelectMultiple)
	name = django_filters.CharFilter(lookup_expr='icontains', label='Nazwa zawiera')
	#published_year = django_filters.NumberFilter(name='publieshed', lookup_expr='year')
	class  Meta:
		model = Library
		fields = ['status','type', 'chain','state','name',]

