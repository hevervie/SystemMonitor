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

    def verification(self, username, password):
        """用户名密码验证函数"""
        try:
            passwd = login.objects.get(name=username).passwd
            print(passwd)
            if passwd == password:
                return 1, 'success'
            else:
                return 0, 'username or password error!'
        except login.DoesNotExist as d:  # 如果不存在,则会抛出DoesNotExist异常
            return -1, d
        except login.MultipleObjectsReturned as m:  # 如果返回多个，则会抛出MultipleObjectsReturned异常
            return -2, m
        except Exception as e:
            return -3, e

    def get_all(self):
        all_user = login.objects.all()
        user = {}
        for i in all_user:
            user[i.name] = i.passwd
        return user


# /*=====================================================*/
# /*     table: user            用户信息                */
# /*=====================================================*/

class user(models.Model):
    user_id = models.IntegerField()
    email = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user_id
