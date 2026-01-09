"""
feellist APP的服务基类：封装通用的业务逻辑
新手必看：
- 连接视图层和仓储层
- 复用分页、筛选的通用逻辑
"""
from abc import ABC
from typing import Dict, List, Tuple, Any

from core.constants.core_constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from core.utils.core_pagination import paginate_data
from feellist.repositories.base import BaseRepository


class BaseService(ABC):
    """
    服务基类：定义APP内所有服务的标准接口
    """
    repository: BaseRepository = None

    def __init__(self):
        if self.repository is None:
            raise NotImplementedError("子类必须指定repository属性")

    def get_list(
            self,
            filters: Dict = None,
            page: int = DEFAULT_PAGE,
            page_size: int = DEFAULT_PAGE_SIZE
    ) -> Tuple[List[Any], int, bool]:
        """
        获取列表数据（筛选+分页）
        :param filters: 筛选条件
        :param page: 页码
        :param page_size: 每页条数
        :return: (分页后的数据列表, 总条数, 是否有筛选条件)
        """
        filters = filters or {}
        # 步骤1：仓储层筛选数据
        data_list, has_filter = self.repository.filter(filters)
        # 步骤2：分页处理
        paginated_data, total = paginate_data(data_list, page, page_size)
        return paginated_data, total, has_filter

    def get_detail(self, pk: int) -> Any:
        """
        获取单条数据详情
        :param pk: 主键ID
        :return: 数据对象
        """
        return self.repository.get_by_id(pk)

    def create(self, data: Dict) -> Any:
        """
        新增数据
        :param data: 新增数据
        :return: 新增的对象
        """
        return self.repository.create(data)

    def update(self, pk: int, data: Dict) -> Any:
        """
        修改数据
        :param pk: 主键ID
        :param data: 修改数据
        :return: 修改后的对象
        """
        return self.repository.update(pk, data)

    def delete(self, pk: int) -> bool:
        """
        删除数据
        :param pk: 主键ID
        :return: True
        """
        return self.repository.delete(pk)
