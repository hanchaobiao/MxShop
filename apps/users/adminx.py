#!/usr/bin/env python
# encoding: utf-8

# Xadmin会自动搜寻这种命名的文件。
import xadmin
from xadmin import views
from .models import VerifyCode
from users.models import UserProfile, VerifyCode
from trade.models import OrderGoods, ShoppingCart
"""
将全局配置修改:
    如左上角：django Xadmin。下面的我的公司
    主题修改，app名称汉化，菜单收叠
"""


# 创建Xadmin的全局管理器并与view绑定。
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# x admin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "慕学生鲜后台"
    # 最下面我的公司
    site_footer = "mxshop"
    # menu_style = "accordion"
    # 收起菜单
    # menu_style = "accordion"

    # def get_site_menu(self):
    #     return (
    #         {'title': '交易管理',
    #          'menus': (
    #              {'title': '购物车', 'url': self.get_model_url(ShoppingCart, 'changelist')},
    #              {'title': '订单', 'url': self.get_model_url(OrderGoods, 'changelist')},
    #          )},
    #         {'title': '商品管理',
    #          'menus': (
    #              {'title': '所在城市', 'url': self.get_model_url(CityDict, 'changelist')},
    #              {'title': '机构讲师', 'url': self.get_model_url(Teacher, 'changelist')},
    #              {'title': '机构信息', 'url': self.get_model_url(CourseOrg, 'changelist')},)},
    #         {'title': '用户管理',
    #          'menus': (
    #              {'title': '用户信息', 'url': self.get_model_url(UserProfile, 'changelist')},
    #              {'title': '用户验证', 'url': self.get_model_url(EmailVerifyRecord, 'changelist')},
    #              {'title': '用户课程', 'url': self.get_model_url(UserCourse, 'changelist')},
    #              {'title': '用户收藏', 'url': self.get_model_url(UserFavorite, 'changelist')},
    #              {'title': '用户消息', 'url': self.get_model_url(UserMessage, 'changelist')},
    #          )},
    #         {'title': '系统管理',
    #          'menus': (
    #              {'title': '用户咨询', 'url': self.get_model_url(UserAsk, 'changelist')},
    #              {'title': '首页轮播', 'url': self.get_model_url(Banner, 'changelist')},
    #              {'title': '用户分组', 'url': self.get_model_url(Group, 'changelist')},
    #              {'title': '用户权限', 'url': self.get_model_url(Permission, 'changelist')},
    #              {'title': '日志记录', 'url': self.get_model_url(Log, 'changelist')},
    #          )},
    #     )


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]


# 将后台管理器与models进行关联注册。
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
# 将全局配置管理与view绑定注册
xadmin.site.register(views.BaseAdminView, BaseSetting)
#  将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView, GlobalSettings)
