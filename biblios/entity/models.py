#from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from django.db import models
#from uuid import UUID

# Create your models here.
class Adress(models.Model):
	STATUS = (
('N','Nieaktywny'),
('A','Aktywny')
		)
	status = models.CharField(max_length=1, choices=STATUS, verbose_name="Status")
	street = models.CharField(max_length=128, verbose_name="Ulica",default="Ulica" )
	zip_code = models.CharField(max_length=5, verbose_name="Kod pocztowy", default="00000") 
	city = models.CharField(max_length=50, verbose_name="Miasto", default="Miasto")
	state = models.CharField(max_length=50, verbose_name=u"Województwo", default="Mazowieckie")       
	


	def _unicode_(self):
		return self.street

class Email(models.Model):
	STATUS = (
('N','Nieaktywny'),
('A','Aktywny')
		)
	status = models.CharField(max_length=1, choices=STATUS, verbose_name="Status", default="N")
	email = models.EmailField(max_length=254, verbose_name="adres e-mail", default="adres@email.pl")


	def _unicode_(self):
		return self.email

class Biblioteka(models.Model):
	name = models.CharField(max_length=200, verbose_name="Nazwa instytucji", default="Biblioteka")
	#adres = models.ForeignKey(Adress, on_delete=models.CASCADE)
	phone = models.CharField(max_length=10, verbose_name="Telefon", default="+48123456789")
	published = models.DateTimeField(verbose_name="Data wprowadzenia")
	url = models.URLField(max_length=200, verbose_name="Strona internetowa", default="https://")
	#email=models.ManyToManyField(Email)
	#email = models.ForeignKey(Email, on_delete=models.CASCADE, default="adres@email.pl")
	TYPE = (
('P','Pbliczna'),
('N','Naukowa')
		)
	type = models.CharField(max_length=1, choices=TYPE, verbose_name="Typ biblioteki")
	CHAIN = (
('P','Pbliczna'),
('N','Naukowa')
		)
	chain = models.CharField(max_length=1, choices=CHAIN, verbose_name=u"Sieć bibliotek")
	owner = models.CharField(max_length=100, verbose_name="Organizator")
	siglum = models.CharField(max_length=15, verbose_name="Siglum", default="WA N")
	notes = models.TextField(verbose_name="Uwagi")
	slug = models.SlugField(max_length=50)
	#uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	def _unicode_(self):
		return self.name




		