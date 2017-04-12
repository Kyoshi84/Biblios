#from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import datetime
from haystack import indexes
from biblios.models import Library
from biblios.models import Adress

class LibraryIndex (indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    published = indexes.DateTimeField(model_attr='published')
    phone = indexes.CharField(model_attr='phone')
    email = indexes.CharField(model_attr='email')
    url = indexes.CharField(model_attr='url')
    type = indexes.CharField(model_attr='type')
    chain = indexes.CharField(model_attr='chain')
    owner = indexes.CharField(model_attr='owner')
    siglum = indexes.CharField(model_attr='siglum')


    def get_model(self):
        return Library

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())

#        name = models.CharField(max_length=200, verbose_name="Nazwa instytucji", default="Biblioteka")
#	phone = models.CharField(max_length=10, verbose_name="Telefon", default="+48123456789")
#	published = models.DateTimeField(verbose_name="Data wprowadzenia")
#	url = models.URLField(max_length=200, verbose_name="Strona internetowa", default="https://")
#	email = models.EmailField(max_length=25, verbose_name="Email", default="adres@email.pl")
#	TYPE = (
#('P','Pbliczna'),
#('N','Naukowa')
#		)
#	type = models.CharField(max_length=1, choices=TYPE, verbose_name="Typ biblioteki")
#	CHAIN = (
#('P','Pbliczna'),
#('N','Naukowa')
#		)
#	chain = models.CharField(max_length=1, choices=CHAIN, verbose_name=u"Sieć bibliotek")
#	owner = models.CharField(max_length=100, verbose_name="Organizator")
#	siglum = models.CharField(max_length=15, verbose_name="Siglum", default="WA N")
#	notes = models.TextField(verbose_name="Uwagi")
#	slug = models.SlugField(max_length=50)