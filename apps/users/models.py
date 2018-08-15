from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# 扩充系统django user表, 继承django 点进AbstractUser可以看到这个models里面就有我们默认表的那些字段。
# 需要去 settings 中配置 AUTH_USER_MODEL
class UserProfile(AbstractUser):
    """
    用户(继承AbstractUser)
    """
    # 自定义的性别选择规则
    # null=True, blank=True 设置可以为空
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    # meta信息，即后台栏目名
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


