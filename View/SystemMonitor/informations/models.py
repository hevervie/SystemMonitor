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
    irp = models.DecimalField(max_digits=16, decimal_places=2)
    softirq = models.DecimalField(max_digits=16, decimal_places=2)
    steal = models.DecimalField(max_digits=16, decimal_places=2)
    guest = models.DecimalField(max_digits=16, decimal_places=2) 
    guest_nice = models.DecimalField(max_digits=16, decimal_places=2)

# /*=====================================================*/
# /*     table: svmem            物理内存信息             */
# /*=====================================================*/
# class svmem(models.Model):
#     total = models.