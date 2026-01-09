"""
项目级全局异常处理：所有APP的接口抛出异常，都会统一格式返回
新手必看：
- 不用在每个接口里写try-except
- 抛出这里的异常类，接口会自动返回标准错误格式
"""
from rest_framework import status
from rest_framework.exceptions import APIException

from core.constants.core_constants import (
    HTTP_BAD_REQUEST, HTTP_NOT_FOUND, HTTP_UNAUTHORIZED,
    MSG_PARAM_ERROR, MSG_DATA_NOT_FOUND, MSG_PERMISSION_DENIED
)


class BaseAPIException(APIException):
    """
    异常基类：所有自定义异常都继承这个类
    """

    def __init__(self, detail=None, code=None):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code

    @property
    def status_code(self):
        """返回对应的DRF状态码"""
        code_map = {
            HTTP_BAD_REQUEST: status.HTTP_400_BAD_REQUEST,
            HTTP_NOT_FOUND: status.HTTP_404_NOT_FOUND,
            HTTP_UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
        }
        return code_map.get(self.code, status.HTTP_400_BAD_REQUEST)


# ==================== 常用自定义异常 ====================
class ParamError(BaseAPIException):
    """参数错误异常"""
    default_detail = MSG_PARAM_ERROR
    default_code = HTTP_BAD_REQUEST


class DataNotFoundError(BaseAPIException):
    """数据不存在异常"""
    default_detail = MSG_DATA_NOT_FOUND
    default_code = HTTP_NOT_FOUND


class PermissionDeniedError(BaseAPIException):
    """权限不足异常"""
    default_detail = MSG_PERMISSION_DENIED
    default_code = HTTP_UNAUTHORIZED
