from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Library, Home
import django_filters
from .filters import LFilter
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string

# Create your views here.

#def index(request):
 #  return HttpResponse("Hello, world. You're at the contacts index.")


def index(request):
	#full list
	queryset_list = Library.objects.all()
	#search
	query = request.GET.get('q', '')
	if query:
		queryset_list = queryset_list.filter(
			Q(name__icontains=query)|
			Q(phone__icontains=query)|
			Q(url__icontains=query)| 
			Q(email__icontains=query)| 
			Q(owner__icontains=query)
				).distinct()
		
	library_list = Library.objects.all()
	library_filter = LFilter(request.GET, queryset=library_list)
	
	#pagination
	paginator = Paginator(queryset_list, 10)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		"object_list": queryset, 
		"name" : "List",
		"page_request_var": page_request_var,
		"filter": library_filter,
			}
		
	
	return render(request, 'index.html', context, {'filter': library_filter})			

def home(request):
	return render_to_response('home.html',{'home': Home.objects.all()})	

def contact(request):
	library_list = Library.objects.all()
	library_filter = LFilter(request.GET, queryset=library_list)
	return render(request, 'contact.html', {'filter': library_filter})
	

# to jest zle, do poprawy view dla pojedynczego rekordu
def entity(request, library_id):
	try:
		library = Library.objects.get(pk=library_id)
	except Library.DoesNotExist:
		raise Http404("Biblioteka o takim id nie istnieje")	
	# response = "Wyniki dla bibliotekki %s."
	return render(request, 'entity.html', {'library': library})

def html_to_pdf_view(request):
    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    html_string = render_to_string('core/pdf_template.html', {'paragraphs': paragraphs})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response