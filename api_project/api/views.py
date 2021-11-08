from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def listing(request):
    message = "Hello Test API"
    return HttpResponse(message)