#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: 韩朝彪
# @Date  : 2018/8/12
# @Desc  :
import time
from rest_framework import serializers
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializer


class ShopCartDetailSerializer(serializers.ModelSerializer):
    """
    序列化，类似于form，restful api
    """
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车序列化
        如果继承的是ModelSerializer，在进行添加重复商品时在is_valid时其联合唯一索引unique_together = ("user", "goods")
        就会报错，不会进入create方法，无法进行对购物车已存在的商品进行修改数量操作。
    使用ModelSerializer外键序列化可以通过 goods = GoodsSerializer方式
    但使用Serializer，外键序列化只能通过goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())
    ModelSerializer：重载了create,update方法
    Serializer：只是定义了方法，需要我们自己重载
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    nums = serializers.IntegerField(min_value=1, required=True, error_messages={
        "min_value": "商品最小值为1",
        "required": "请选择商品数量"
    })
    # 由于继承的是Serializer 不是ModelSerializer， 所以需要配置queryset

    # 这样设置只是在选中商品时，接口文档中可以根据商品名称下拉选择所有商品，序列化是仅仅返回goods_is
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
            """
            重写create方法，在添加前判断商品是否已经在购物车里，如果已存在，只在修改商品数量
            :param validated_data: 
            :return: 
            """
            # serializer中, request在上下文中
            user = self.context["request"].user
            # validated_data是经过验证后的数据
            goods = validated_data['goods']
            nums = validated_data['nums']
            existed = ShoppingCart.objects.filter(user=user, goods=goods)

            if existed:
                existed = existed[0]
                existed.nums += nums
                existed.save()
            else:
                existed = ShoppingCart.objects.create(**validated_data)
            return existed

    def update(self, instance, validated_data):
        """
        重载update，Serializer类必须重载
        :param instance: 类的实例
        :param validated_data: 
        :return: 
        """
        instance.nums = validated_data['nums']
        instance.save()
        return instance

    class Meta:
        model = ShoppingCart
        fields = ('user', 'goods', 'nums')


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    订单详情
    """
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    """
    订单详情
    """
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    """
    订单
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True, format="%Y%m%d %H:%M:%S")
    add_time = serializers.DateTimeField(read_only=True, format="%Y%m%d %H:%M:%S")

    def generate_order_sn(self):
        """
        生成订单号 当前时间+user_id+随机数
        :return: 
        """
        from random import Random
        rand = Random()
        order_sn = "{time_str}{user_id}{rand_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                          user_id=self.context['request'].user.id,
                                                          rand_str=rand.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        """
        修改order_sn
        :param attrs: 
        :return: 
        """
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
