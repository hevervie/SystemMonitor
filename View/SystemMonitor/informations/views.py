from django.shortcuts import render
from django.http import HttpResponse
from informations.models import sdiskio


def test(request):
    diskio = sdiskio.objects.all()
    html = ""
    return HttpResponse(html)

# Create your views here.
