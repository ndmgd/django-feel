"""
项目级通用分页工具：所有APP的列表接口都能用这个分页
新手必看：
- 支持所有可迭代对象（列表、查询集等）
- 自动处理页码越界、每页条数超限
"""
from typing import List, Tuple, Any

from core.constants.core_constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from core.exceptions.core_exceptions import ParamError


def paginate_data(
        data: List[Any],
        page: int = DEFAULT_PAGE,
        page_size: int = DEFAULT_PAGE_SIZE
) -> Tuple[List[Any], int]:
    """
    通用分页函数
    :param data: 要分页的原始数据列表
    :param page: 当前页码
    :param page_size: 每页条数
    :return: (分页后的数据列表, 总条数)
    :raise ParamError: 页码或每页条数非法时抛出异常
    """
    # 步骤1：校验并转换分页参数
    try:
        page_int = int(page) if page else DEFAULT_PAGE
        page_size_int = int(page_size) if page_size else DEFAULT_PAGE_SIZE
    except (ValueError, TypeError):
        raise ParamError(detail="页码和每页条数必须是整数")

    # 步骤2：限制每页条数的范围
    page_size_int = max(1, min(page_size_int, MAX_PAGE_SIZE))
    # 步骤3：限制页码的范围（至少是第1页）
    page_int = max(1, page_int)

    # 步骤4：计算切片范围
    total = len(data)
    start = (page_int - 1) * page_size_int
    end = start + page_size_int

    # 步骤5：处理页码越界（比如只有10条数据，查第2页，每页10条 → 返回空列表）
    if start >= total:
        return [], total

    # 步骤6：返回分页数据和总条数
    return data[start:end], total
