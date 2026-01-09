"""
项目级通用参数工具：所有APP的接口都能用这个清洗、校验参数
新手必看：
- 去掉参数空格、转换类型、校验格式
- 不用在每个接口里写重复的校验代码
"""
from typing import Dict, Any

from core.constants.core_constants import MSG_INT_PARAM_INVALID, MSG_STR_PARAM_INVALID
from core.exceptions.core_exceptions import ParamError


def clean_request_params(request_params: Dict, mapping: Dict = None) -> Dict:
    """
    清洗请求参数
    1. 去掉字符串参数的首尾空格
    2. 映射前端参数名到后端字段名（比如前端传phonenuber→后端用phone_number）
    :param request_params: 原始请求参数（比如request.GET）
    :param mapping: 参数名映射字典，格式：{"前端参数名": "后端字段名"}
    :return: 清洗后的参数字典
    """
    mapping = mapping or {}
    cleaned = {}

    for key, value in request_params.items():
        # 步骤1：映射参数名
        backend_key = mapping.get(key, key)
        # 步骤2：清洗值
        if isinstance(value, str):
            cleaned_value = value.strip()
        else:
            cleaned_value = value
        # 步骤3：非空值才保留
        if cleaned_value is not None and cleaned_value != "":
            cleaned[backend_key] = cleaned_value

    return cleaned


def validate_int(value: Any, param_name: str = "参数") -> int:
    """
    校验并转换为整数
    :param value: 要校验的值
    :param param_name: 参数名（用于错误提示）
    :return: 整数
    :raise ParamError: 校验失败抛出异常
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ParamError(detail=MSG_INT_PARAM_INVALID % param_name)


def validate_str(value: Any, param_name: str = "参数") -> str:
    """
    校验并转换为字符串
    :param value: 要校验的值
    :param param_name: 参数名
    :return: 字符串
    :raise ParamError: 校验失败抛出异常
    """
    if value is None:
        raise ParamError(detail=MSG_STR_PARAM_INVALID % param_name)
    return str(value).strip()


# ==================== 业务常用校验函数 ====================
def validate_phone(value: str) -> str:
    """
    校验手机号格式
    """
    value = validate_str(value, "手机号")
    if len(value) != 11 or not value.isdigit():
        from core.constants import MSG_PHONE_INVALID
        raise ParamError(detail=MSG_PHONE_INVALID)
    return value


def validate_city(value: Any) -> int:
    """
    校验地市ID（必须是整数）
    """
    return validate_int(value, "地市ID")


def validate_cell_id(value: Any) -> int:
    """
    校验小区ID（必须是整数）
    """
    return validate_int(value, "小区ID")
