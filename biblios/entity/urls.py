from django.conf.urls import url
import views
#import admin
import entity

urlpatterns = [ 
	url(r'^$', views.list, name='entity'),
	url(r'^date/$', views.current_datetime, name='date'),
	]