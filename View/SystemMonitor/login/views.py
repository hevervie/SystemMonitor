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
            type = user().get_type_by_id(rtu)
            request.session['username'] = username
            if type == 0:
                return HttpResponseRedirect('/root/')
            elif type == 1:
                return HttpResponseRedirect('/employee/')
            elif type == 2:
                return HttpResponseRedirect('//sysadm/')
            else:
                return HttpResponse("Error")
        elif rtu <= 0:
            render = {
                'url': '..',
                'message': '用户名或密码错误！'
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
    if request.POST:
        user_num = request.session['username']
        old_passwd = request.POST['old_passwd']
        new_passwd = request.POST['new_passwd']
        confirm_passwd = request.POST['confirm_passwd']

        rtu = user().is_num_exist(user_num)
        if new_passwd != confirm_passwd:
            return render_to_response('root/passwd.html', {'message': "两次输入的密码相同！"},
                                      context_instance=RequestContext(request))
        if rtu > 0:
            rtu, message = login().passwd_alter(rtu, new_passwd, old_passwd)
            if rtu == 1:
                return render_to_response('root/passwd.html', {'message': user_num + "密码修改成功！"},
                                          context_instance=RequestContext(request))
            else:
                return render_to_response('root/passwd.html', {'message': "密码修改失败！" + message},
                                          context_instance=RequestContext(request))
    return render_to_response('root/passwd.html', {}, context_instance=RequestContext(request))


def login_root(request):
    type_1 = user().get_user_number_by_type(1)
    type_2 = user().get_user_number_by_type(2)
    return login_base(request, 'root/index.html', {'high_manager': type_1, 'common_manager': type_2})


def login_add(request):
    if request.POST:
        num = request.POST['num']
        name = request.POST['name']
        type = int(request.POST['type'])
        email = request.POST['email']
        if len(num) < 8 or len(num.strip()) < 8:
            message = "工号长度错误，须为8位数字！"
        elif len(name) < 1 or len(name) > 20:
            message = "姓名过长或过短！"
        elif type != 1 and type != 2:
            message = "角色类型不合法！"
        elif len(email) < 1:
            message = "邮箱不能为空！"
        else:
            u = user()
            if u.is_num_exist(num) == 0:
                u.user_add(num, type, name, email)
                message = num + "添加成功！"
                return render_to_response('root/add.html', {'message': message},
                                          context_instance=RequestContext(request))
            else:
                message = num + "已存在，请重试！"
                return render_to_response('root/add.html', {'message': message},
                                          context_instance=RequestContext(request))
        render = {
            'message': message,
            'num': num,
            'name': name,
            'email': email,
        }
        return render_to_response('root/add.html', render, context_instance=RequestContext(request))
    else:
        return render_to_response('root/add.html', {}, context_instance=RequestContext(request))


def login_manage(request):
    message = ""
    if request.POST:
        user_id = int(request.POST['id'])
        sign, message = user().delete_user_by_id(user_id)
        u = user().get_all_user()
        if sign == 1:
            message = "删除成功！"
        else:
            message = "删除失败:"
        return render_to_response('root/manage.html',
                                  {'user': u, 'type1': '一般运维', 'type2': '系统管理员', 'message': message,
                                   'count': len(u) - 1},
                                  context_instance=RequestContext(request))
    else:
        pass
        u = user().get_all_user()
        return render_to_response('root/manage.html',
                                  {'user': u, 'type1': '一般运维', 'type2': '系统管理员', 'message': message,
                                   'count': len(u) - 1},
                                  context_instance=RequestContext(request))


def login_alter(request):
    render = {}
    if request.POST:
        user_id = request.POST['id']
        if 'num' in request.POST.keys():
            num = request.POST['num']
            name = request.POST['name']
            type = int(request.POST['type'])
            email = request.POST['email']

            render = {
                'user_id': user_id,
                'num': num,
                'name': name,
                'email': email,
            }

            if len(num) < 8 or len(num.strip()) < 8:
                message = "工号长度错误，须为8位数字！"
            elif len(name) < 1 or len(name) > 20:
                message = "姓名过长或过短！"
            elif type != 1 and type != 2:
                message = "角色类型不合法！"
            elif len(email) < 1:
                message = "邮箱不能为空！"
            else:
                u = user()
                sign, mess = u.user_alter(user_id, num, type, name, email)
                if sign == 1:
                    message = num + "修改成功！"
                    render['message'] = message
                else:
                    message = num + "失败，请重试！"
                    render['message'] = message
            return render_to_response('root/alter.html', render, context_instance=RequestContext(request))
        else:
            u = user().get_user_by_id(user_id)
            if u:
                render = {
                    'user_id': user_id,
                    'num': u.user_num,
                    'user_type': u.user_type,
                    'name': u.name,
                    'email': u.email,
                }
            return render_to_response('root/alter.html', render, context_instance=RequestContext(request))
    else:
        pass
    return render_to_response('root/alter.html', render, context_instance=RequestContext(request))


def test(request):
    return HttpResponse('success')
