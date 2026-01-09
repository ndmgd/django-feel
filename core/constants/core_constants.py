"""
项目级全局常量：所有APP都能用，不用重复定义
新手必看：
- 响应码、提示语、分页默认值，全项目统一
- 改这里的内容，所有APP的接口都会生效
"""
# ==================== 响应状态码 ====================
HTTP_SUCCESS = 200  # 请求成功
HTTP_CREATED = 201  # 新增成功
HTTP_NO_CONTENT = 204  # 删除成功
HTTP_BAD_REQUEST = 400  # 参数错误/请求错误
HTTP_UNAUTHORIZED = 401  # 未登录/权限不足
HTTP_NOT_FOUND = 404  # 数据不存在
HTTP_SERVER_ERROR = 500  # 服务器内部错误

# ==================== 通用提示语 ====================
# 成功提示
MSG_SUCCESS = "操作成功"
MSG_QUERY_SUCCESS = "查询成功"
MSG_CREATE_SUCCESS = "新增成功"
MSG_UPDATE_SUCCESS = "修改成功"
MSG_DELETE_SUCCESS = "删除成功"

# 错误提示
MSG_ERROR = "操作失败"
MSG_PARAM_ERROR = "参数格式错误"
MSG_VALIDATE_ERROR = "数据验证失败"
MSG_DATA_NOT_FOUND = "数据不存在"
MSG_PERMISSION_DENIED = "权限不足"
MSG_SERVER_ERROR = "服务器内部错误"

# ==================== 分页默认配置 ====================
DEFAULT_PAGE = 1  # 默认页码
DEFAULT_PAGE_SIZE = 10  # 默认每页条数
MAX_PAGE_SIZE = 100  # 最大每页条数（防止一次查太多数据）

# ==================== 参数校验提示语 ====================
MSG_INT_PARAM_INVALID = "%s必须是整数"
MSG_STR_PARAM_INVALID = "%s必须是字符串"
MSG_PHONE_INVALID = "请输入有效的11位手机号"
MSG_EMAIL_INVALID = "请输入有效的邮箱地址"
