from django.shortcuts import render
import time
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShopCartDetailSerializer, OrderInfoSerializer, OrderInfoDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车管理
    list:
        购物车详情
    delete:
        删除购物车商品
    create:
        新增商品
    update:
        修改购物车
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    IsAuthenticated = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = ShoppingCartSerializer

    # 删除，修改操作根据goods_id搜索
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderInfoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                       mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    订单管理
    list:
        订单列表
    create:
        新增订单
    delete:
        取消订单
    retrieve:
        订单详情
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    IsAuthenticated = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderInfoDetailSerializer
        else:
            return OrderInfoSerializer

    def perform_create(self, serializer):
        """
        重写perform_create，在数据保存之前作如下操作
        1、生成订单号                
        :param serializer: 
        :return: 
        """
        order = serializer.save()
        # 获取购物车添加到订单商品中
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_good = OrderGoods()
            order_good.goods = shop_cart.goods
            order_good.goods_num = shop_cart.nums
            order_good.order = order

            order_good.save()
            shop_cart.delete()
