from django.shortcuts import render_to_response
from django.http import HttpResponse
from informations.models import *


# Create your views here.
def adm_index(request):
    pass


def ajax_test(request):
    cpu = scputimes.objects.all()[0,9]

    for item in cpu:


