#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : permissions.py
# @Author: 韩朝彪
# @Date  : 2018/8/7
# @Desc  : 自定义权限
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    django 如果未登录只能访问安全方法，登录后才能进行post,delete等操作，且只能删除自己的数据
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user
