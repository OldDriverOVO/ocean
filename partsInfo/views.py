from django.shortcuts import render
from django.http import HttpResponse

# Create your partinfo here.

def index(request):

    return render(request, 'partinfo/index.html')

def parts(request):

    return render(request, 'partinfo/parts_list.html')
