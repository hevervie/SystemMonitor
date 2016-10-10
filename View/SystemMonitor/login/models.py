from django.db import models


# Create your models here.

# /*=====================================================*/
# /*     table: login            用户登录                */
# /*=====================================================*/

class login(models.Model):
    name = models.CharField(max_length=20)
    passwd = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


# /*=====================================================*/
# /*     table: user            用户信息                */
# /*=====================================================*/

class user(models.Model):
    user_id = models.IntegerField()
    email = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user_id
