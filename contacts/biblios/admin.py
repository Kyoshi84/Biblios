# -*- coding: utf-8 -*-
from django.contrib import admin
from actions import export_to_csv
from .models import Library, Home
from datetime import datetime
from django import forms
from redactor.widgets import RedactorEditor
from .models import Home

# Register your models here.


#class AdressInline(admin.TabularInline):
#	model = Adress
class LibraryAdmin(admin.ModelAdmin):
#	inlines = [
#	AdressInline	
#	]

	list_display = ['name', 'type','url','email', 'published','city', 'state', 'street', 'zip_code', 'status',]
	list_display_links = ['name']
	search_fields = ['name', 'type', 'phone', 'url','email', 'siglum', 'owner', 'published', 'city', 'state', 'status', 'street', 'zip_code',]
	list_filter = ['status', 'city']
#class AdressAdmin(admin.ModelAdmin):
#	list_display = ['name', 'city', 'state', 'street', 'zip_code', 'status']	
#	list_display_links = ['name']
#	search_fields = ['library__name','city', 'state', 'status', 'street', 'zip_code',]
#	list_filter = ['status', 'library__name']
	def name(self, obj):
		return obj.library.name
		name.admin_order_field  = 'name'  #Allows column order sorting
    	name.short_description = 'Biblioteka'  #Renames column head

	actions = [export_to_csv(filename='library')]
	def get_field2(self, obj):
		return obj.field2

    #Filtering on side - for some reason, this works
    
class HomeAdmin(admin.ModelAdmin):
	class Meta:
		model = Home
		widgets = {
		'short_text': RedactorEditor(),
					}
	list_display = ['title']
	list_display_links = ['title']
	search_fields = ['title', 'content']



admin.site.register(Library, LibraryAdmin,)
admin.site.register(Home, HomeAdmin)

