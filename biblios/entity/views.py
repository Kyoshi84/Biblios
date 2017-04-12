from django.http import HttpResponse
import datetime
import entity

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def list(request):
     return HttpResponse("Hello, world. You're at the polls index.")