from django.shortcuts import render
from django.http import HttpResponse
from ad.models import *

# Create your views here.
def main_view(request):
    # context = {'phrase': 'hello world'}
    # return HttpResponse("Hello, Django!")

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html')