from django.shortcuts import render_to_response
from django.template import RequestContext
from login.models import login, user
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


def login_base(request, template, dict):
    return render_to_response(template, dict)


def login_passwd(request):
    return login_base(request, 'root/passwd.html', {})


def login_root(request):

    return login_base(request, 'root/index.html', {})


def login_add(request):
    if request.POST:
        num = request.POST['num']
        name = request.POST['name']
        type = request.POST['type']
        email = request.POST['email']
        u = user()

        if u.is_num_exist(num) == 0:
            u.user_add(num, type, name, email)
            message = num + "添加成功！"
            return render_to_response('root/add.html', {'message': message}, context_instance=RequestContext(request))
        else:
            message = num + "已存在，请重试！"
            return render_to_response('root/add.html', {'message': message}, context_instance=RequestContext(request))
    else:
        return render_to_response('root/add.html', {}, context_instance=RequestContext(request))


def login_manage(request):
    return login_base(request, 'root/manage.html', {})


def login_alter(request):
    return login_base(request, 'root/alter.html', {})


def test(request):
    user().user_add('04143153', 1, 'ZhouPan', 'zhoupan@xiyoulinux.org')
    return HttpResponse('success')
