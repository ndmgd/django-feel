"""
NetworkSceneData 业务服务：封装小区场景数据相关的业务逻辑
"""
from typing import Dict

from feellist.repositories.network_scene import NetworkSceneDataRepository
from feellist.services.base import BaseService


class NetworkSceneDataService(BaseService):
    """
    NetworkSceneData 业务服务类
    """
    repository = NetworkSceneDataRepository()

    # ==================== 通用业务方法 ====================
    def get_city_complaint_rate(self, city: int) -> float:
        """
        计算指定地市的投诉率
        投诉率 = 有投诉小区数 / 总小区数 * 100%
        """
        # 获取指定地市的所有数据
        all_data = list(self.repository.filter({"city": city}))[0]
        if not all_data:
            return 0.0
        # 获取有投诉的数据
        complaint_data = self.repository.get_complaint_data_by_city(city)
        # 计算投诉率
        complaint_rate = (len(complaint_data) / len(all_data)) * 100
        return round(complaint_rate, 2)

    # ==================== 扩展业务方法 ====================
    def get_scene_distribution(self, city: int) -> Dict[int, int]:
        """
        获取指定地市的场景分布统计
        返回格式：{场景ID: 小区数量}
        """
        data_list = list(self.repository.filter({"city": city}))[0]
        distribution = {}
        for item in data_list:
            scene_id = item.scene_level1
            distribution[scene_id] = distribution.get(scene_id, 0) + 1
        return distribution
