#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : serializer.py
# @Author: 韩朝彪
# @Date  : 2018/8/7
# @Desc  :  序列化
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
import re
from .models import UserFav, UserLeavingMessage, UserAddress
from MxShop.settings import REGEX_MOBILE


class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏商品序列化
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 设置隐藏字段，默认值当前用户，在接口文档中不要用户提交user信息

    class Meta:
        model = UserFav
        fields = ('user', 'goods', 'id')
        # 自己定义唯一性验证，多字段验证，没法指定某一个字段出错，其字段名是non_field_errors
        validators = [UniqueTogetherValidator(queryset=UserFav.objects.all(), fields=("user", "goods"), message="已经收藏")]


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言序列化
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")  # 该值只返回，不提交，返回时格式化时间

    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'message_type', 'subject', 'message', 'file', 'add_time')


class UserAddressSerializer(serializers.ModelSerializer):
    """
    收货地址序列化
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # 该值只返回，不提交，返回时格式化时间
    # add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    def validate_signer_mobile(self, signer_mobile):
        """
        验证手机号
        :param signer_mobile: 
        :return: 
        """
        # 验证是否合法
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码不合法")
        return signer_mobile

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile')
