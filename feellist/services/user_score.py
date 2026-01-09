"""
UserScore 业务服务：封装用户评分相关的业务逻辑
新手必看：
- 视图层只调用这里的方法，不直接操作数据库
- 复杂业务逻辑写在这里，比如计算平均分
"""
from typing import List

from feellist.models import UserScore
from feellist.repositories.user_score import UserScoreRepository
from feellist.services.base import BaseService


class UserScoreService(BaseService):
    """
    UserScore 业务服务类
    """
    repository = UserScoreRepository()  # 注入仓储实例

    # ==================== 通用业务方法 ====================
    def calculate_city_avg_score(self, city: int) -> float:
        """
        计算指定地市的平均小区评分
        :param city: 地市ID
        :return: 平均分（保留2位小数）
        """
        # 调用仓储层获取数据
        data_list = self.repository.get_by_city_and_net_type(city, net_type=1)  # 假设查5G数据
        if not data_list:
            return 0.0
        # 计算有效评分的平均值
        valid_scores = [item.cell_score for item in data_list if item.cell_score is not None]
        if not valid_scores:
            return 0.0
        avg_score = sum(valid_scores) / len(valid_scores)
        return round(avg_score, 2)

    # ==================== 扩展业务方法 ====================
    def get_top_score_cells(self, city: int, top_n: int = 10) -> List[UserScore]:
        """
        获取指定地市评分最高的N个小区
        """
        data_list = self.repository.get_by_city_and_net_type(city, net_type=1)
        # 按评分排序，取前N个
        sorted_list = sorted(data_list, key=lambda x: x.cell_score or 0, reverse=True)
        return sorted_list[:top_n]
