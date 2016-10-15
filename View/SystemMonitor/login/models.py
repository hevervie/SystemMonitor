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

    def get_type_num(self):
        all_user = self.objects.all()
        type_1 = 0
        type_2 = 0
        type_3 = 0
        for i in all_user:
            if i.user_type == 1:
                type_1 += 1
            elif i.user_type == 2:
                type_2 += 1
            else:
                type_3 += 1
        return type_1, type_2, type_3

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
            passwd = login.objects.get(id=user.objects.get(user_num=username).id).passwd
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

    def get_login_by_user_id(self, user_id):
        try:
            return 1, login.objects.get(user_id=user_id)
        except Exception as e:
            return 0, e

    def passwd_alter(self, user_id, passwd):
        rtu, l = login().get_login_by_user_id(user_id)
        if rtu == 1:
            l.passwd = passwd
            return 1, "success"
        else:
            return 0, str(l)
