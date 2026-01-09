"""
项目级通用权限类：所有APP的接口都能复用
新手必看：
- 控制哪些用户能访问哪些接口
- 支持匿名访问、登录用户访问、管理员访问
"""
from rest_framework.permissions import BasePermission

from core.constants.core_constants import MSG_PERMISSION_DENIED


class AllowAny(BasePermission):
    """
    允许任何人访问（比如公开接口）
    """
    message = MSG_PERMISSION_DENIED

    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    """
    必须登录才能访问
    """
    message = MSG_PERMISSION_DENIED

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAdminUser(BasePermission):
    """
    必须是管理员才能访问
    """
    message = MSG_PERMISSION_DENIED

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
