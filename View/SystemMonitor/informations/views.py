from django.shortcuts import render_to_response
from django.http import HttpResponse
from informations.models import *
import simplejson


# Create your views here.
def adm_index(request):
    pass


def ajax_test(request):
    cpu = scputimes.objects.all()[0:9]
    data = []
    for item in cpu:
        d = {'user': item.user, 'nice': item.nice, 'system': item.system, 'guest': item.guest}
        data.append(simplejson.dumps(d))
    render = {
        'data': data
    }
    return render_to_response('admin/test/ajax.html', render)
