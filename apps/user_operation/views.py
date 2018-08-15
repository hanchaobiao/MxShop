from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
# Create your views here.
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserLeavingMessageSerializer, UserAddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    retrieve: 
        获取收藏相信信息
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    destroy:
        删除收藏商品
    """

    # drf权限认证 IsAuthenticated：已登录
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    # 配置认证方式,需经过jwt验证或session验证（开发时方便测试保留session验证）
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 设置详细信息根据goods_id查找，不是根据pk(主键), lookup_field是在queryset结果里进行筛选
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user).all()


class LeavingMessageViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        留言列表
    destroy:
        删除留言
    create:
        添加留言
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserLeavingMessageSerializer

    def get_queryset(self):
        """
        重写该方法，只返回当前用户留言信息
        :return: 
        """
        return UserLeavingMessage.objects.filter(user=self.request.user).all()


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    收货地址操作
    list:
        收货地址列表
    create:
        新增收货地址
    destroy:
        删除收货地址
    update:
        修改收货地址
    partial_update:
        修改收货地址
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).all()
