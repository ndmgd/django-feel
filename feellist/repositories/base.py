"""
feellist APP的仓储基类：封装通用的数据库操作
新手必看：
- 所有业务仓储都继承这个类
- 不用重复写增删改查的基础代码
"""
from abc import ABC
from typing import Dict, List, Tuple, Type

from django.db import models

from core.exceptions.core_exceptions import DataNotFoundError


class BaseRepository(ABC):
    """
    仓储基类：定义APP内所有仓储的标准接口
    """
    # 子类必须指定对应的Django模型
    model: Type[models.Model] = None

    def __init__(self):
        if self.model is None:
            raise NotImplementedError("子类必须指定model属性")

    def get_all(self, order_by: str = "-id") -> List[models.Model]:
        """
        查询所有数据
        :param order_by: 排序字段，默认按ID倒序
        :return: 模型对象列表
        """
        return list(self.model.objects.all().order_by(order_by))

    def filter(self, filters: Dict, order_by: str = "-id") -> Tuple[List[models.Model], bool]:
        """
        条件筛选
        :param filters: 筛选条件字典
        :param order_by: 排序字段
        :return: (模型对象列表, 是否有筛选条件)
        """
        queryset = self.model.objects.all().order_by(order_by)
        has_filter = False

        # 应用筛选条件
        for key, value in filters.items():
            if hasattr(self.model, key):
                queryset = queryset.filter(**{key: value})
                has_filter = True

        return list(queryset), has_filter

    def get_by_id(self, pk: int) -> models.Model:
        """
        按ID查询单条数据
        :param pk: 主键ID
        :return: 模型对象
        :raise DataNotFoundError: 数据不存在时抛出异常
        """
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise DataNotFoundError(detail=f"ID为{pk}的数据不存在")

    def create(self, data: Dict) -> models.Model:
        """
        新增数据
        :param data: 新增数据字典
        :return: 新增的模型对象
        """
        return self.model.objects.create(**data)

    def update(self, pk: int, data: Dict) -> models.Model:
        """
        修改数据
        :param pk: 主键ID
        :param data: 修改数据字典
        :return: 修改后的模型对象
        :raise DataNotFoundError: 数据不存在时抛出异常
        """
        obj = self.get_by_id(pk)
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, pk: int) -> bool:
        """
        删除数据
        :param pk: 主键ID
        :return: True（删除成功）
        :raise DataNotFoundError: 数据不存在时抛出异常
        """
        obj = self.get_by_id(pk)
        obj.delete()
        return True
