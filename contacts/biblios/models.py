#from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
import django_filters
from django.forms import TextInput, Textarea
from django import forms
from redactor.fields import RedactorField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.



class Library(models.Model):
	class Meta:
		verbose_name = _("Biblioteka")
		verbose_name_plural = _("Biblioteki")
		

	name = models.CharField(max_length=200, verbose_name="Nazwa instytucji", default="Biblioteka")
	phone = PhoneNumberField(verbose_name="Telefon", default="+48123456789")
	published = models.DateTimeField(verbose_name="Data wprowadzenia")
	url = models.URLField(max_length=200, verbose_name="Strona internetowa", default="https://")
	email = models.EmailField(max_length=25, verbose_name="Email", default="adres@email.pl")
	TYPE_CHOICES = (
	('P','Pbliczna'),
	('N','Naukowa')
       	)
	type = models.CharField(max_length=1, choices=TYPE_CHOICES, verbose_name="Typ biblioteki")
	CHAIN_CHOICES = (
	('P','Pbliczna'),
	('N','Naukowa')
       	)
	chain = models.CharField(max_length=1, choices=CHAIN_CHOICES, verbose_name=u"Sieć bibliotek")
	owner = models.CharField(max_length=100, verbose_name="Organizator")
	siglum = models.CharField(max_length=15, verbose_name="Siglum", default="WA N")
	notes = RedactorField(verbose_name="Uwagi")
	slug = models.SlugField(max_length=50)
	street = models.CharField(max_length=128, verbose_name="Ulica",default="Ulica" )
	zip_code = models.CharField(max_length=5, verbose_name="Kod pocztowy", default="00000") 
	city = models.CharField(max_length=50, verbose_name="Miasto", default="Miasto")
	STATE_CHOICES = (
	('0',u'Dolnośląskie'),
	('1','Kujawsko-pomorskie'),
	('2','Lubelskie'),
	('3','Lubuskie'),
	('4',u'Łódzkie'),
	('5',u'Małopolskie'),
	('6','Mazowieckie'),
	('7','Opolskie'),
	('8','Podkarpackie'),
	('9','Podlaskie'),
	('10','Pomorskie'),
	('11',u'Śląskie'),
	('12',u'Świętokrzyskie'),
	('13',u'Warmińsko-mazurskie'),
	('14','Wielkopolskie'),
	('15','Zachodniopomorskie')
		)
	state = models.CharField(max_length=50, choices=STATE_CHOICES, verbose_name=u"Województwo", default="Mazowieckie") 
	STATUS_CHOICES = (
	('N','Nieaktywny'),
	('A','Aktywny')
       )
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="Status", default="A")

	def _unicode_(self):
		return self.name
	def _str_(self):
		return self.name




class Home(models.Model):
	class Meta:
		verbose_name = _("Home")
		verbose_name_plural = _("Strona startowa")
	title = models.CharField(max_length=100, verbose_name="Tytuł")
	content = RedactorField(max_length=1000, verbose_name="Zawartość" )
#	
	def _unicode_(self):
		return self.title

#	def _str_(self):
#		return self.name