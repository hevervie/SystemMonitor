from django.shortcuts import render_to_response
from django.http import HttpResponse
from informations.models import *
import simplejson


# Create your views here.

def adm_index(request):
    render = {
        'number': client().get_host_number()
    }
    return render_to_response('admin/index.html', render)


def ajax_test(request):
    # cpu = scputimes.objects.all()[0:9]
    alarm_info = alarm.objects.all().order_by("-id")[0:10]
    data = []
    for item in alarm_info:
        recv = receive.objects.get(id=item.recv_id)
        d = {'cpu': item.svmem, 'date': recv.datetime.strftime("%Y-%m-%d"), 'time': recv.datetime.strftime("%H:%M:%S")}
        data.append(simplejson.dumps(d))
    render = {
        'data': data
    }
    return render_to_response('admin/test/ajax.html', render)
