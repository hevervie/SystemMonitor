"""SystemMonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from informations.views import *
from login.views import *

urlpatterns = [
    url(r'^admin/$', include(admin.site.urls)),
    # url(r'^test/$', ajax_test),

]
login = [
    url(r'^root/$', login_root),
    url(r'^root/passwd/$', login_passwd),
    url(r'^root/manager/$', login_manage),
    url(r'^root/add/$', login_add),
    url(r'^root/alter/$', login_alter),
    url(r'^root/delete/$', login_delete),
    url(r'^root/test', test),
    url(r'^$', user_login)
]

informations = [
    url(r'^sysadm/$', admin_index),
    url(r'^sysadm/json', admin_index_json),
    url(r'^sysadm/cpu/$', cpu),
    url(r'^sysadm/memory/$', memory),
    url(r'^sysadm/disk/$', disk),
    url(r'^sysadm/network/$', network),
    url(r'^sysadm/loginuser/$', loginuser),
    url(r'^sysadm/port/$', port),
    url(r'^sysadm/test/$', admin_test),
]

urlpatterns += login
urlpatterns += informations
