"""
NetworkSceneData 业务仓储：专门处理小区场景数据表的数据库操作
"""
from typing import Dict, List, Tuple

from core.utils.core_filters import (
    validate_city, validate_cell_id, validate_int
)
from feellist.models import NetworkSceneData
from feellist.repositories.base import BaseRepository


class NetworkSceneDataRepository(BaseRepository):
    """
    NetworkSceneData 仓储类
    """
    model = NetworkSceneData

    def filter(self, filters: Dict, order_by: str = "-id") -> Tuple[List[NetworkSceneData], bool]:
        """
        重写筛选方法：添加NetworkSceneData特有的参数校验
        """
        validated_filters = {}
        # 基础筛选条件校验
        if "city" in filters:
            validated_filters["city"] = validate_city(filters["city"])
        if "cell_id" in filters:
            validated_filters["cell_id"] = validate_cell_id(filters["cell_id"])
        # 业务特有筛选条件校验
        if "has_complaint" in filters:
            validated_filters["has_complaint"] = validate_int(filters["has_complaint"], "投诉状态")
        if "scene_level1" in filters:
            validated_filters["scene_level1"] = validate_int(filters["scene_level1"], "场景类型")
        if "area" in filters:
            validated_filters["area"] = validate_int(filters["area"], "区域类型")

        return super().filter(validated_filters, order_by)

    # ==================== NetworkSceneData 特有方法 ====================
    def get_complaint_data_by_city(self, city: int) -> List[NetworkSceneData]:
        """
        查询指定地市的有投诉数据
        """
        city = validate_city(city)
        return list(self.model.objects.filter(city=city, has_complaint=1).order_by("-create_time"))
