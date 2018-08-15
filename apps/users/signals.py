#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : signals.py
# @Author: 韩朝彪
# @Date  : 2018/8/5
# @Desc  : django 信号量 signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # 信号量，在创建时修改密码
        # instance 就是User对象
        password = instance.password
        instance.set_password(password)
        instance.save()
