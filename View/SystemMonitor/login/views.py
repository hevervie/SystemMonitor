from login.models import login, user
from django.http import HttpResponseRedirect, HttpResponse
from login.mymako import render_mako_context
import simplejson


def login_index(request):
    render = {
        'url': '.',
        'message': ''
    }
    return render_mako_context(request, 'login.html', render)


def user_login(request):
    request.encoding = 'utf-8'
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        rtu, message = login().verification(username, password)
        if rtu > 0:
            type = user().get_type_by_id(rtu)
            request.session['userid'] = user().get_user_by_id(rtu).id
            if type == 1:  # 系统管理员
                return HttpResponseRedirect('/root/')
            elif type == 2:  # 高级运维人员
                return HttpResponseRedirect('/employee/')
            elif type == 3:  # 一般运维人员
                return HttpResponseRedirect('/sysadm/')
            else:
                return HttpResponse("Error")
        else:
            render = {
                'message': '用户名或密码错误！'
            }
            return render_mako_context(request, 'login.html', render)
    else:
        render = {
            'message': ''
        }
        return render_mako_context(request, 'login.html', render)


def login_base(request, template, dict):
    return render_mako_context(request, template, dict)


def login_passwd(request):
    u = user().get_user_by_id(request.session['userid'])
    if request.POST:
        origin = request.POST['origin']
        new = request.POST['new']
        repeat = request.POST['repeat']
        if new != repeat:
            rtu = {
                'status': False,
                'message': "两次输入的密码不相同！"
            }
            return HttpResponse(simplejson.dumps(rtu))
        result, mess = login().passwd_alter(u.id, new, origin)
        if result == 0:
            rtu = {
                'status': False,
                'message': mess
            }
            return HttpResponse(simplejson.dumps(rtu))
        else:
            rtu = {
                'status': True,
                'message': 'success'
            }
            return HttpResponse(simplejson.dumps(rtu))

    return render_mako_context(request, 'root/passwd.html', {'users': u})


def login_root(request):
    userid = request.session['userid']
    type_1 = user().get_user_number_by_type(2)
    type_2 = user().get_user_number_by_type(3)
    return render_mako_context(request, 'root/index.html',
                               {'users': user().get_user_by_id(userid), 'high_manager': type_1,
                                'common_manager': type_2})


def login_add(request):
    users = user().get_user_by_id(request.session['userid'])
    if request.POST:
        num = request.POST['num']
        name = request.POST['name']
        type = int(request.POST['type'])
        email = request.POST['mail']
        if len(num) < 8 or len(num.strip()) < 8:
            message = "工号长度错误，须为8位数字！"
        elif len(name) < 1 or len(name) > 20:
            message = "姓名过长或过短！"
        elif type != 1 and type != 2 and type != 3:
            message = "角色类型不合法！"
        elif len(email) < 1:
            message = "邮箱不能为空！"
        else:
            usr = user()
            if usr.is_num_exist(num) == 0:
                usr.user_add(num, type, name, email)
                print(num)
                rtu = {
                    'status': True,
                    'message': 'success'
                }
                return HttpResponse(simplejson.dumps(rtu))
            else:
                message = num + "已存在，请重试！"
                rtu = {
                    'status': False,
                    'message': message
                }
                return HttpResponse(simplejson.dumps(rtu))
        rtu = {
            'status': False,
            'message': message
        }
        return HttpResponse(simplejson.dumps(rtu))
    else:
        return render_mako_context(request, 'root/add.html', {'users': users})


def login_manage(request):
    message = ""
    u = user().get_user_by_id(request.session['userid'])
    if request.POST:
        user_id = int(request.POST['id'])
        sign, message = user().delete_user_by_id(user_id)
        users = user().get_all_user()
        if sign == 1:
            message = "删除成功！"
        else:
            message = "删除失败:"
        return render_mako_context(request, 'root/manage.html',
                                   {'alluser': users, 'users': u, 'message': message})
    else:
        pass
        users = user().get_all_user()
        return render_mako_context(request, 'root/manage.html',
                                   {'alluser': users, 'users': u, 'message': message})


def login_alter(request):
    # 获取当前用户信息
    u = user().get_user_by_id(request.session['userid'])
    # 对信息进行更改
    if request.POST:
        user_id = request.POST['id']
        num = request.POST['num']
        name = request.POST['name']
        type = int(request.POST['type'])
        email = request.POST['mail']

        if len(num) < 8 or len(num.strip()) < 8:
            message = "工号长度错误，须为8位数字！"
        elif len(name) < 1 or len(name) > 20:
            message = "姓名过长或过短！"
        elif type != 1 and type != 2 and type != 3:
            message = "角色类型不合法！"
        elif len(email) < 1:
            message = "邮箱不能为空！"
        else:
            u = user()
            sign, mess = u.user_alter(user_id, num, type, name, email)
            if sign == 1:
                rtu = {
                    'status': True,
                    'message': "success"
                }
                return HttpResponse(simplejson.dumps(rtu))
            else:
                rtu = {
                    'status': False,
                    'message': mess
                }
                return HttpResponse(simplejson.dumps(rtu))
        rtu = {
            'status': False,
            'message': message
        }
        return HttpResponse(simplejson.dumps(rtu))

    elif request.GET:
        if 'id' in request.GET.keys():
            usr = user().get_user_by_id(request.GET['id'])
            render = {
                'users': u,
                'id': usr.id,
                'user_num': usr.user_num,
                'type': usr.user_type,
                'name': usr.name,
                'email': usr.email,
            }
            return render_mako_context(request, 'root/alter.html', render)
        else:
            pass
    return HttpResponseRedirect("/root")


def login_delete(request):
    """对用户进行删除"""
    if request.POST:
        id = request.POST['id']
        sign, mess = user().delete_user_by_id(id)
        if sign == 1:
            rtu = {
                'status': True,
                'message': "success"
            }
            return HttpResponse(simplejson.dumps(rtu))
        else:
            rtu = {
                'status': False,
                'message': mess
            }
            return HttpResponse(simplejson.dumps(rtu))
    else:
        return HttpResponseRedirect("/root/")


def test(request):
    id = request.POST['id']
    return HttpResponse(simplejson.dumps({'status': True, 'message': 'success'}))
