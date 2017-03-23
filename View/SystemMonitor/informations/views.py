from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from informations.models import *
from login.models import user
import simplejson
from informations.mymako import render_mako_context


# Create your views here.
def admin_index(request):
    userid = request.session['userid']
    warning = warn()
    recv = receive()
    all = warning.get_warn_count_by_status()
    deal = warning.get_warn_count_by_status(status=1)  # 1：已处理,0 ：未处理
    untreate = warning.get_warn_count_by_status(status=0)
    rundays = recv.get_run_days()
    return render_mako_context('/admin', 'admin/index.html', {
        'users': user().get_user_by_id(userid),
        'all': all,
        'deal': deal,
        'untreate': untreate,
        'rundays': rundays
    })


def admin_index_json(request):
    if request.GET:
        if request.GET['type'] == 'warn':
            warning = warn()
            now = datetime.datetime.now().strftime("%Y-%m-%d")
            yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            date_now = []
            time_now = []
            date_yestd = []
            time_yestd = []
            data_now = []
            data_yestd = []
            for i in range(0, 25, 2):
                if i < 10:
                    str_now = now + " %d:00:00" % i
                    str_yestd = yesterday + " %d:00:00" % i
                    date_now.append(str_now)
                    time_now.append("0%d:00" % i)
                    date_yestd.append(str_yestd)
                    time_yestd.append("0%d:00" % i)
                else:
                    str_now = now + " %d:00:00" % i
                    str_yestd = yesterday + " %d:00:00" % i
                    date_now.append(str_now)
                    time_now.append("%d:00" % i)
                    date_yestd.append(str_yestd)
                    time_yestd.append("%d:00" % i)
            date_now.pop()
            date_yestd.pop()
            date_now.append(now + " 23:59:59")
            date_yestd.append(yesterday + " 23:59:59")
            for i in range(0, 12, 1):
                data_now.append(warning.get_warn_by_time_count(date_now[i], date_now[i + 1]))
                data_yestd.append(warning.get_warn_by_time_count(date_yestd[i], date_yestd[i + 1]))
            json = {
                "code": 0,
                "result": True,
                "message": "success",
                "data": {

                    "series": [
                        {
                            "name": yesterday + "告警监测",
                            "color": "red",
                            "data": data_yestd
                        },
                        {
                            "name": now + "告警监测",
                            "color": "orange",
                            "data": data_now
                        }
                    ],
                    "categories": time_now
                }
            }
            return HttpResponse(simplejson.dumps(json))
    else:
        return HttpResponseRedirect("/")


def cpu(request):
    userid = request.session['userid']
    u = user().get_user_by_id(userid)
    return render_mako_context(request, 'admin/cpu.html', {'users': u})


def memory(request):
    userid = request.session['userid']
    u = user().get_user_by_id(userid)
    return render_mako_context(request, 'admin/memory.html', {'users': u})


def disk(request):
    userid = request.session['userid']
    u = user().get_user_by_id(userid)
    return render_mako_context(request, 'admin/disk.html', {'users': u})


def network(request):
    userid = request.session['userid']
    u = user().get_user_by_id(userid)
    return render_mako_context(request, 'admin/network.html', {'users': u})


def loginuser(request):
    userid = request.session['userid']
    u = user().get_user_by_id(userid)
    return render_mako_context(request, 'admin/loginuser.html', {'users': u})


def port(request):
    userid = request.session['userid']
    u = user().get_user_by_id(userid)
    return render_mako_context(request, 'admin/port.html', {'users': u})


def admin_test(request):
    return render_mako_context(request, 'admin/test/include.html', {'title': 'include.html'})
