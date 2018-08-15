#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: 韩朝彪
# @Date  : 2018/8/5
# @Desc  :
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import re
from datetime import datetime, timedelta
from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode


User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    类似于form，验证后端提交的字段，并且可将查询结果序列化
    """

    mobile = serializers.CharField(required=True, max_length=11, help_text="手机号")

    def validated_mobile(self, mobile):
        """
        验证手机号码
        :param mobile: 
        :return: 
        """
        # 验证是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")

        # 验证是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("手机号码已经注册")

        # 验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60秒")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """
    class Meta:
        model = User
        fields = ('name', 'birthday', 'gender', 'email')


class UserRegSerializer(serializers.ModelSerializer):
    # 在user表基础上扩展认证字段 write_only:设置后，序列化时不会读取返回该字段，因为后面我们进行了del code 因此，
    # 需设置write_only,不然在序列化时获取code时会报错
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, help_text="验证码",
                                 label="验证码",
                                 error_messages={  # 自定义错误消息
                                     "required": "验证码不能为空",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 })
    # 唯一性验证
    username = serializers.CharField(required=True, allow_blank=False, label="用户名", help_text="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    # 考虑到安全性，密码不应该返回
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, label="密码", help_text="密码")

    # TODO 这里使用了信号量，在添加用户前对密码进行了加密，在signals文件中（使用重载create方法也可以）

    # def create(self, validated_data):
    #     """
    #     重载
    #     :param validated_data:
    #     :return:
    #     """
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_code = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by("-add_time")
        if verify_code:
            last_code = verify_code[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if last_code.add_time < five_mintes_ago:
                raise serializers.ValidationError("验证码过期")
            if last_code.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        """
        作用于所有字段之上, 验证通过将code删除，设置mobile
        :param attrs: 
        :return: 
        """
        attrs['mobile'] = attrs['username']
        del attrs['code']  # 不保存数据库中
        return attrs

    class Meta:
        model = User
        fields = ('username', 'password', 'mobile', 'code')
