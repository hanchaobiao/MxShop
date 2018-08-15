#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : filters.py
# @Author: 韩朝彪
# @Date  : 2018/8/4
# @Desc  :  定义搜索过滤条件

from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")  # icontains模糊查询， i忽略大小写
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr="gte")
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr="lte")
    top_category = filters.NumberFilter(field_name='category', method='top_category_filter')  # 自定义过滤方法

    def top_category_filter(self, queryset, name, value):
        """
        商品类别过滤
        :param queryset: 
        :param name: 
        :param value: 
        :return: 
        """
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot']
