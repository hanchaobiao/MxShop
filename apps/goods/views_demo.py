from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
# Create your views here.

from .models import Goods
from .serializers import GoodsSerializer
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    """
    自定义分页
    """
    page_size = 10  # 默认每页10条
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100  # 最大一百条


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    实现商品列表分页，过滤，搜索，排序
    """
    # 返回结果变量名必须为queryset
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    # 使用filter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')
    search_fields = ('^name', 'goods_desc', 'goods_brief')  # 搜索过滤字段
    ordering_fields = ('shop_price', 'add_time')
    filterset_class = GoodsFilter  # 引用自定义filter类
    # def get_queryset(self):
    #     # 重写get_queryset方法实现过滤
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get('price_min', 0)
    #     if price_min:
    #         # gt > gte >=
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset

# class GoodsListView(generics.ListAPIView):
#     # 返回结果变量名必须为queryset
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination

#
# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     # 返回结果变量名必须为queryset
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# class GoodsListView(APIView):
#     """
#     商品操作
#     """
#     def get(self, request, format=None):
#         """
#         查看商品列表
#         :param request:
#         :param format:
#         :return:
#         """
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)
#
#     def post(self, request, format=None):
#         """
#         新增一个商品
#         :param request:
#         :return:
#         """
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

