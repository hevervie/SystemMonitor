from django.db import models


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


# /*=====================================================*/
# /*     table: receive            接收到的信息           */
# /*=====================================================*/

class receive(models.Model):
    client_id = models.IntegerField()
    cpu_id = models.IntegerField()
    svmem_id = models.IntegerField()
    sswap_id = models.IntegerField()
    diskio_id = models.IntegerField()
    diskusage_id = models.IntegerField()
    netio_type = models.IntegerField()
    user_type = models.IntegerField()
    port_type = models.IntegerField()

    def __unicode__(self):
        return self.id


# /*=====================================================*/
# /*     table: alarm            警告信息                 */
# /*=====================================================*/

class alarm(models.Model):
    recv_id = models.IntegerField()
    client_id = models.IntegerField()
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
