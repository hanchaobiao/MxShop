#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : serializer.py
# @Author: 韩朝彪
# @Date  : 2018/8/2
# @Desc  :  序列化类
from rest_framework import serializers
from .models import Goods
from .models import GoodsCategory, GoodsImage


class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    商品分类第三类别
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    商品分类第二类别
    """

    sub_cat = GoodsCategorySerializer3(many=True)  # 获取二类标题下的三级类别，让返回结果有层次嵌套

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    注意这里为什么吗用sub_cat， 应为在model中这个外键的related_name="sub_cat", 必须与其保持一致，由于一级别类向下会有多个二级类别，
    必须配置many=True
    """
    sub_cat = GoodsCategorySerializer2(many=True)  # 获取一类列表下的二级类别，让返回结果有层次嵌套

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsImage
        fields = ('image', )  # 只序列化images


class GoodsSerializer(serializers.ModelSerializer):
    """
    序列化，类似于form，restful api
    """
    category = GoodsCategorySerializer()  # 默认会显示外键id，配置后会显示GoodsCategory对象所有信息
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ('name', 'click_num', 'market_price', 'add_time')
        fields = "__all__"

    def create(self, validated_data):
        return Goods.objects.create(**validated_data)

