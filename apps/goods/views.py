from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import View
from django.http import JsonResponse
from rest_framework import filters
from rest_framework import generics, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
# Create your views here.
from django.db.models import Min, Max
from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, GoodsCategorySerializer
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    """
    自定义商品分页
    """
    page_size = 10  # 默认每页10条
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100  # 最大一百条


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    实现商品列表分页，过滤，搜索，排序，商品详情
    list:
        实现商品列表分页，过滤，搜索，排序
    retrieve:
        商品详情
    """
    # RetrieveModelMixin 详情
    # ListModelMixin 列表

    # 返回结果变量名必须为queryset
    queryset = Goods.objects.all()
    # 序列化返回值
    serializer_class = GoodsSerializer
    # 分页
    pagination_class = GoodsPagination
    # 配置token认证
    # authentication_classes = (TokenAuthentication, )
    # 使用filter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')
    filterset_class = GoodsFilter  # 引用自定义filter类
    search_fields = ('^name', 'goods_desc', 'goods_brief')  # 搜索过滤字段
    ordering_fields = ('sold_num', 'shop_price')  # 排序

    def list(self, request, *args, **kwargs):
        """
        重载方法， 返回商品价格最大值，动态调整价格区间
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        queryset = self.filter_queryset(self.get_queryset())
        # 理解aggregate的关键在于理解SQL中的聚合函数：以下摘自百度百科：SQL基本函数，聚合函数对一组值执行计算，并返回单个值。
        # 除了 COUNT 以外，聚合函数都会忽略空值。 常见的聚合函数有AVG / COUNT / MAX / MIN /SUM 等。
        # 如果你想要对数据进行分组（GROUP BY）后再聚合的操作，则需要使用annotate来实现
        price_max = queryset.aggregate(price_max=Max('shop_price'))
        serializer = self.get_serializer(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            re_dict = response.data
            # 实现在分页结果返回值中添加一个新的key: val
            price_range = []
            start = 0
            step = price_max['price_max']/4
            import math
            for i in range(0, 4):
                end = math.ceil(start+step)
                price_range.append({"min": start, "max": end})
                start = end
            re_dict['priceRange'] = price_range
            return Response(re_dict)

        # re_dict = serializer.data
        # re_dict['price_max'] = price_max
        return Response(serializer.data)

# class GoodsPriceRangeView(View):
#     """
#     商品价格最大值
#     """
#     def get(self, request):
#         price_max = Goods.objects.values('shop_price').annotate(Max('shop_price'))
#         data = {"price_max": price_max}
#         return JsonResponse(data, safe=False)


class GoodsCategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取商品类别
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1).all()
    serializer_class = GoodsCategorySerializer

