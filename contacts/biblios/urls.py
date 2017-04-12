from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^entity/(?P<library_id>\d+)/$', views.entity, name='entity'),
    url(r'^kontakt/$', views.contact, name='kontakt'),
    ]