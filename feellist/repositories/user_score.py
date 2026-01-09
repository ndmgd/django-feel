"""
UserScore 业务仓储：专门处理用户评分表的数据库操作
新手必看：
- 继承BaseRepository，复用基础增删改查
- 只需要写UserScore特有的筛选逻辑
"""
from typing import Dict, List, Tuple

from core.utils.core_filters import validate_city, validate_cell_id, validate_phone
from feellist.models import UserScore
from feellist.repositories.base import BaseRepository


class UserScoreRepository(BaseRepository):
    """
    UserScore 仓储类
    """
    model = UserScore  # 指定对应的模型

    def filter(self, filters: Dict, order_by: str = "-id") -> Tuple[List[UserScore], bool]:
        """
        重写筛选方法：添加UserScore特有的参数校验
        """
        # 步骤1：参数校验（转换为正确的类型）
        validated_filters = {}
        if "city" in filters:
            validated_filters["city"] = validate_city(filters["city"])
        if "cell_id" in filters:
            validated_filters["cell_id"] = validate_cell_id(filters["cell_id"])
        if "phone_number" in filters:
            validated_filters["phone_number"] = validate_phone(filters["phone_number"])
        if "net_type" in filters:
            validated_filters["net_type"] = validate_cell_id(filters["net_type"])  # net_type也是整数

        # 步骤2：调用父类的filter方法执行筛选
        return super().filter(validated_filters, order_by)

    # ==================== UserScore 特有方法 ====================
    def get_by_city_and_net_type(self, city: int, net_type: int) -> List[UserScore]:
        """
        按地市和网络类型查询
        """
        city = validate_city(city)
        net_type = validate_cell_id(net_type)
        return list(self.model.objects.filter(city=city, net_type=net_type).order_by("-create_time"))
