#  from django.http import HttpResponse
from django.shortcuts import render
def homepage(request):
    # return HttpResponse("Wello Horld!")
    return render(request, 'home.html')


def about(request):
    # return HttpResponse("This page is about Junior Journey!")
    return render(request, 'about.html')

def pdf_compressor(request):
    return render(request, 'pdf_compressor.html')

def not_found(request):
    return render(request, '404.html')