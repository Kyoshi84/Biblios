from django.contrib import admin
from .models import Biblioteka	
from .models import Adress
# Register your models here.
#admin.site.register(models.Biblioteka) - it works z bardzo generycznym widokiem
class BibliotekaAdmin(admin.ModelAdmin):
    pass
    list_filter = ['type']
admin.site.register(Biblioteka)