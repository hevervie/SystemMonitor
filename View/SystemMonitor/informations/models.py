from django.db import models
from django.utils import timezone
import datetime
from django.db import connection


# Create your models here.
#
# /*=====================================================*/
# /*     table:  scputimes           CPU信息             */
# /*=====================================================*/

class scputimes(models.Model):
    user = models.DecimalField(max_digits=16, decimal_places=2)
    nice = models.DecimalField(max_digits=16, decimal_places=2)
    system = models.DecimalField(max_digits=16, decimal_places=2)
    idle = models.DecimalField(max_digits=16, decimal_places=2)
    iowait = models.DecimalField(max_digits=16, decimal_places=2)
    irq = models.DecimalField(max_digits=16, decimal_places=2)
    softirq = models.DecimalField(max_digits=16, decimal_places=2)
    steal = models.DecimalField(max_digits=16, decimal_places=2)
    guest = models.DecimalField(max_digits=16, decimal_places=2)
    guest_nice = models.DecimalField(max_digits=16, decimal_places=2)

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table: svmem            物理内存信息             */
# /*=====================================================*/
class svmem(models.Model):
    total = models.BigIntegerField()
    available = models.BigIntegerField()
    percent = models.DecimalField(max_digits=16, decimal_places=2)
    used = models.BigIntegerField()
    free = models.BigIntegerField()
    active = models.BigIntegerField()
    inactive = models.BigIntegerField()
    buffers = models.BigIntegerField()
    cached = models.BigIntegerField()
    shared = models.BigIntegerField()

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table: sswap            虚拟内存信息             */
# /*=====================================================*/

class sswap(models.Model):
    total = models.BigIntegerField()
    used = models.BigIntegerField()
    free = models.BigIntegerField()
    percent = models.DecimalField(max_digits=16, decimal_places=2)
    sin = models.IntegerField()
    sout = models.IntegerField()

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table: sdiskio            磁盘IO                */
# /*=====================================================*/


class sdiskio(models.Model):
    device = models.CharField(max_length=20, blank=True, null=True)
    read_count = models.BigIntegerField()
    write_count = models.BigIntegerField()
    read_bytes = models.BigIntegerField()
    write_bytes = models.BigIntegerField()
    read_time = models.BigIntegerField()
    write_time = models.BigIntegerField()
    read_merged_count = models.BigIntegerField()
    write_merged_count = models.BigIntegerField()
    busy_time = models.BigIntegerField()

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table: sdiskusage            磁盘分区使用率      */
# /*=====================================================*/

class sdiskusage(models.Model):
    point = models.CharField(max_length=20)
    total = models.BigIntegerField()
    used = models.BigIntegerField()
    free = models.BigIntegerField()
    percent = models.DecimalField(max_digits=16, decimal_places=2)

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table: snetio            网络IO                 */
# /*=====================================================*/

class snetio(models.Model):
    device = models.CharField(max_length=20)
    type = models.IntegerField()
    bytes_sent = models.BigIntegerField()
    bytes_recv = models.BigIntegerField()
    packets_sent = models.BigIntegerField()
    packets_recv = models.BigIntegerField()
    errin = models.BigIntegerField()
    errout = models.BigIntegerField()
    dropin = models.BigIntegerField()
    dropout = models.BigIntegerField()

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table: suser            用户信息                */
# /*=====================================================*/

class suser(models.Model):
    type = models.IntegerField()
    name = models.CharField(max_length=20)
    terminal = models.CharField(max_length=20)
    host = models.CharField(max_length=15)
    started = models.DecimalField(max_digits=16, decimal_places=2)

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table: sport            端口信息                 */
# /*=====================================================*/

class sport(models.Model):
    type = models.IntegerField()
    port = models.IntegerField()

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table:client             客户端列表              */
# /*=====================================================*/

class client(models.Model):
    host = models.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return self.host

    def get_host_number(self):
        return client.objects.count()


# /*=====================================================*/
# /*     table: receive            接收到的信息           */
# /*=====================================================*/

class receive(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(client)
    cpu = models.ForeignKey(scputimes)
    svmem = models.ForeignKey(svmem)
    sswap = models.ForeignKey(sswap)
    sdiskio = models.ForeignKey(sdiskio)
    sdiskusage = models.ForeignKey(sdiskusage)
    snetio = models.IntegerField()
    suser = models.IntegerField()
    sport = models.IntegerField()

    def __unicode__(self):
        return self.id

    def get_receive_by_time(self, date_from=None, date_to=None):
        cursor = connection.cursor()
        # 都为空
        if date_from is None and date_to is None:
            rtu = receive.objects.all()
            data = []
            for i in rtu:
                data.append(i)
            return data

        elif date_from is None:  # 起始时间为空
            # dt = datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            # return receive.objects.filter(datetime__lt=dt)
            cursor.execute("select * from informations_receive where  datetime > '%s'" % date_from)
            data = []
            for i in cursor:
                data.append(i)
            return data

        elif date_to is None:  # 结束时间为空
            # df = datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            # return receive.objects.filter(datetime__gt=df)
            cursor.execute("select * from informations_receive where  datetime < '%s'" % date_from)
            data = []
            for i in cursor:
                data.append(i)
            return data
        else:  # 都不为空
            # df = datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            # dt = datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            # return receive.objects.filter(datetime__range=(df, dt))
            cursor.execute(
                "select * from informations_receive where  datetime > '%s' and datetime < '%s'" % (date_from, date_to))
            data = []
            for i in cursor:
                data.append(i)
            return data

    def get_receive_by_time_count(self, date_from=None, date_to=None):
        cursor = connection.cursor()
        if date_from is None and date_to is None:
            return receive.objects.all().count()
        elif date_from is None:  # 起始时间为空
            # dt = datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            # return receive.objects.filter(datetime__lt=dt).count()
            return cursor.execute("select * from informations_receive where  datetime > '%s'" % date_from)
        elif date_to is None:  # 结束时间为空
            # df = datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            # return receive.objects.filter(datetime__gt=df).count()
            return cursor.execute("select * from informations_receive where  datetime < '%s'" % date_from)
        else:  # 都不为空
            # df = datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            # dt = datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            # return receive.objects.filter(datetime__range=(df, dt)).count()
            return cursor.execute(
                "select * from informations_receive where  datetime > '%s' and datetime < '%s'" % (
                    date_from, date_to))

    def get_all_receive(self):
        return receive.objects.all()

    def get_run_days(self):
        recv = receive.objects.all()[0]
        df = recv.datetime
        print(df)
        dt = datetime.datetime.now()
        df = datetime.datetime.strptime(df.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        dt = datetime.datetime.strptime(dt.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        return (dt - df).days


# /*=====================================================*/
# /*     table: alarm            警告信息                 */
# /*=====================================================*/

class alarm(models.Model):
    receive = models.ForeignKey(receive)
    client = models.ForeignKey(client)
    cpu = models.DecimalField(max_digits=16, decimal_places=2)
    svmem = models.DecimalField(max_digits=16, decimal_places=2)
    swap = models.DecimalField(max_digits=16, decimal_places=2)
    diskio = models.DecimalField(max_digits=16, decimal_places=2)
    diskusage = models.DecimalField(max_digits=16, decimal_places=2)
    snetio = models.DecimalField(max_digits=16, decimal_places=2)
    level = models.IntegerField()
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.id - 0


# /*=====================================================*/
# /*     table: strategy            告警策略             */
# /*=====================================================*/

class strategy(models.Model):
    type = models.CharField(max_length=20)
    argv = models.IntegerField()

    def __unicode__(self):
        return self.type


# /*=====================================================*/
# /*     table: user            合法用户列表              */
# /*=====================================================*/

class user(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


# /*=====================================================*/
# /*     table: port            合法端口列表              */
# /*=====================================================*/

class port(models.Model):
    port = models.IntegerField()

    def __unicode__(self):
        return self.port


# 告警库，需要告警的保存到此数据库中
class warn(models.Model):
    alarmid = models.ForeignKey(alarm)  # 告警id
    datetime = models.DateTimeField(auto_created=True)  # 告警时间
    status = models.IntegerField(default=0)  # 告警状态 # 0 未处理 1 已处理
    type = models.IntegerField(default=0)  # 告警级别 0 一般 1：重要 2:严重

    def get_warn_count_by_type(self, types=None):
        if types is None:
            return warn.objects.count()
        else:
            return warn.objects.filter(type=types).count()

    def get_warn_by_type(self, types=None):
        if types is None:
            return warn.objects.all()
        else:
            return warn.objects.filter(type=types)

    def get_warn_count_by_status(self, status=None):
        if status is None:
            return warn.objects.count()
        else:
            return warn.objects.filter(status=status).count()

    def get_warn_by_status(self, status=None):
        if status is None:
            return warn.objects.all()
        else:
            return warn.objects.filter(status=status)

    def get_warn_by_time(self, date_from=None, date_to=None):
        # 都为空
        cursor = connection.cursor()
        if date_from is None and date_to is None:
            rtu = warn.objects.all()
            data = []
            for i in rtu:
                data.append(i)
            return data
        elif date_from is None:  # 起始时间为空
            # dt = datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            # return warn.objects.filter(datetime__lt=dt)
            cursor.execute("select * from informations_warn where  datetime > '%s'" % date_from)
            data = []
            for i in cursor:
                data.append(i)
            return data
        elif date_to is None:  # 结束时间为空
            # df = datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            # return warn.objects.filter(datetime__gt=df)
            cursor.execute("select * from informations_warn where  datetime < '%s'" % date_from)
            data = []
            for i in cursor:
                data.append(i)
            return data
        else:  # 都不为空
            # df = datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            # dt = datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            # return warn.objects.filter(datetime__range=(df, dt))
            cursor.execute(
                "select * from informations_warn where  datetime > '%s' and datetime < '%s'" % (date_from, date_to))
            data = []
            for i in cursor:
                data.append(i)
            return data

    def get_warn_by_time_count(self, date_from=None, date_to=None):
        cursor = connection.cursor()
        if date_from is None and date_to is None:
            return warn.objects.all().count()
        elif date_from is None:  # 起始时间为空
            # dt = datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            # return warn.objects.filter(datetime__lt=dt).count()
            return cursor.execute("select * from informations_warn where  datetime > '%s'" % date_from)
        elif date_to is None:  # 结束时间为空
            # df = datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            # return warn.objects.filter(datetime__gt=df).count()
            return cursor.execute("select * from informations_warn where  datetime < '%s'" % date_from)
        else:  # 都不为空
            # df = datetime.datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            # dt = datetime.datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            # return warn.objects.filter(datetime__range=(df, dt)).count()

            return cursor.execute(
                "select * from informations_warn where  datetime > '%s' and datetime < '%s'" % (
                    date_from, date_to))
