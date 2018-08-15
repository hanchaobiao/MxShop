"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
# api文档
from rest_framework.documentation import include_docs_urls, include, url
from rest_framework.routers import DefaultRouter
import xadmin
from MxShop.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
# from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet, GoodsCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, UserAddressViewSet
from trade.views import ShoppingCartViewSet, OrderInfoViewSet

router = DefaultRouter()
# 商品列表
router.register('goods', GoodsListViewSet, base_name="goods")
# 商品列表
router.register('categorys', GoodsCategoryViewSet, base_name="categorys")
# 短信验证码
router.register('code', SmsCodeViewSet, base_name="code")
# 用户操作
router.register('users', UserViewSet, base_name="用户")
# 用户收藏
router.register("userfavs", UserFavViewSet, base_name="usersFavs")
# 用户留言
router.register("messages", LeavingMessageViewSet, base_name="messages")
# 用户地址
router.register("address", UserAddressViewSet, base_name="address")
# 购物车
router.register("shopcarts", ShoppingCartViewSet, base_name="shopcarts")
# 个人订单
router.register("orders", OrderInfoViewSet, base_name="orders")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),

    # 配置drf登录
    path('api-auth/', include('rest_framework.urls')),
    # 注册router, 只支持url()，不支持path
    url(r'^', include(router.urls)),
    # 以及api文档路径
    path('docs/', include_docs_urls(title='慕学生鲜')),
    # drf接口认证模式
    path('api-token-auth/', views.obtain_auth_token),
    # jwt接口认证模式
    path('login/', obtain_jwt_token),
]

# 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
