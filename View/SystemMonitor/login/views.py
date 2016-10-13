from django.shortcuts import render_to_response
from django.template import RequestContext
from login.models import login
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.


def index(request):
    render = {
        'url': '.'
    }
    return render_to_response('login.html', render, context_instance=RequestContext(request))


def user_login(request):
    request.encoding = 'utf-8'

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        rtu, message = login().verification(username, password)
        if rtu > 0:
            request.session['username'] = username
            return HttpResponseRedirect('/root/')
        elif rtu <= 0:
            render = {
                'url': '..',
                'message': 'username or password not incorrect!'
            }
            return render_to_response('login.html', render, context_instance=RequestContext(request))
    else:
        render = {
            'url': '..'
        }
        return render_to_response('login.html', render, context_instance=RequestContext(request))
