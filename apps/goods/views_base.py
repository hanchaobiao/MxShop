#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views_base.py
# @Author: 韩朝彪
# @Date  : 2018/8/1
# @Desc  :  使用普通方式写api接口
from django.views.generic.base import View
from goods.models import Goods
from django.http import HttpResponse, JsonResponse
import json


class GoodsListView(View):

    def get(self, request):
        """
        获取商品列表
        :param request: 
        :return: 
        """
        goods = Goods.objects.all()[:10]
        json_list = []
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)

        # 优化写法 将类对象自动序列号为字典，但无法序列化image file等属性
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_list.append(model_to_dict(good))
        # return HttpResponse(json.dumps(json_list), content_type="application/json")
        # 更优写法 序列化所有字段
        # 存在的问题，1、image,file的路径是相对路径，前端需要处理才能访问，2、字段序列化的方式固定
        from django.core.serializers import serialize
        json_list = serialize("json", goods)  # 返回是字符串
        json_list = json.loads(json_list)
        return JsonResponse(json_list, safe=False)
