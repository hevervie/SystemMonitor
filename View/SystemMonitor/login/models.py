from django.db import models


# Create your models here.

# /*=====================================================*/
# /*     table: user            用户信息                */
# /*=====================================================*/

class user(models.Model):
    user_num = models.CharField(max_length=8)
    user_type = models.IntegerField()
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user_id

    def get_type_by_id(self, user_id):
        try:
            type = user.objects.get(id=user_id).user_type
            return type
        except user.DoesNotExist:
            pass

    def user_add(self, user_num, user_type, user_name, user_email):
        u = user(
            user_num=user_num,
            user_type=user_type,
            name=user_name,
            email=user_email,
        )
        u.save()
        l = login(
            user_id=u,
            passwd='123456'
        )
        l.save()

    def user_alter(self, user_id, user_num, user_type, user_name, user_email):
        try:
            u = user.objects.get(id=user_id)
            u.user_num = user_num
            u.user_type = user_type
            u.name = user_name
            u.email = user_email
            u.save()
            return 1, "success"
        except user.DoesNotExist as d:
            return 0, str(d)
        except Exception as e:
            return 0, str(e)

    def is_num_exist(self, num):
        try:
            u = user.objects.get(user_num=num)
        except user.DoesNotExist:
            return 0
        else:
            return u.id

    def get_all_user(self):
        u = user.objects.all()
        return u

    def get_user_by_id(self, user_id):
        try:
            u = user.objects.get(id=user_id)
            return u
        except Exception:
            pass

    def get_user_number_by_type(self, user_type):
        try:
            u = user.objects.filter(user_type=user_type)
            return len(u)
        except user.DoesNotExist:
            return 0

    def delete_user_by_id(self, user_id):
        message = ""
        sign = -1
        try:
            login.objects.get(user_id=user_id).delete()
            user.objects.get(id=user_id).delete()
        except Exception as e:
            message = str(e)
            sign = 0
        else:
            message = "success"
            sign = 1
        finally:
            return sign, message


# /*=====================================================*/
# /*     table: login            用户登录                */
# /*=====================================================*/

class login(models.Model):
    user_id = models.ForeignKey(user)
    passwd = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

    def verification(self, username, password):
        """用户名密码验证函数"""
        try:
            user_id = user.objects.get(user_num=username).id
            passwd = login.objects.get(id=user_id).passwd
            if passwd == password:
                return user_id, 'success'
            else:
                return 0, 'username or password error!'
        except login.DoesNotExist as d:  # 如果不存在,则会抛出DoesNotExist异常
            return -1, d
        except login.MultipleObjectsReturned as m:  # 如果返回多个，则会抛出MultipleObjectsReturned异常
            return -2, m
        except Exception as e:
            return -3, e

    def get_login_by_user_id(self, user_id):
        try:
            return 1, login.objects.get(user_id=user_id)
        except Exception as e:
            return 0, e

    def passwd_alter(self, user_id, new_passwd, old_passwd):
        rtu, l = login().get_login_by_user_id(user_id)
        if rtu == 1:
            if l.passwd == old_passwd:
                l.passwd = new_passwd
                l.save()
                return 1, "success"
            else:
                return 0, '原始密码错误！'
        else:
            return 0, str(l)
