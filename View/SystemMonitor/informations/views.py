from django.shortcuts import render_to_response
from django.http import HttpResponse


def test(request):
    html = "hello"
    return HttpResponse(html)




# Create your views here.
