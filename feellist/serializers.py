"""
feellist APP的序列化器：负责数据格式转换和验证
新手必看：
- 模型对象 → JSON（给前端）
- 前端JSON → 校验后的数据（给后端）
- 自定义展示字段，比如把city=1转成"南昌市"
"""
from rest_framework import serializers

from core.constants.core_constants import MSG_PHONE_INVALID
from feellist.models import UserScore, NetworkSceneData


# ==================== 工具函数 ====================
def get_choice_name(choices: list, value: int) -> str:
    """
    根据choices和值，获取对应的名称
    """
    choice_dict = dict(choices)
    return choice_dict.get(value, "")


# ==================== UserScore 序列化器 ====================
class UserScoreSerializer(serializers.ModelSerializer):
    """
    UserScore 序列化器
    """
    # 自定义展示字段：把ID转换成名称
    # 自定义字段：展示地市的友好名称（基于模型的choices）
    city_display = serializers.CharField(source='get_city_display', read_only=True)
    # 自定义字段：展示网络类型的友好名称（基于模型的choices）
    net_type_display = serializers.CharField(source='get_net_type_display', read_only=True)
    # 自定义字段：一级场景友好名称
    scene_level1_display = serializers.CharField(source='get_scene_level1_display', read_only=True)

    class Meta:
        model = UserScore
        fields = "__all__"
        # 补充手机号验证
        extra_kwargs = {
            "phone_number": {
                "error_messages": {
                    "invalid_phone": MSG_PHONE_INVALID
                }
            }
        }


# ==================== NetworkSceneData 序列化器 ====================
class NetworkSceneDataSerializer(serializers.ModelSerializer):
    """
    NetworkSceneData 序列化器
    """
    # 自定义展示字段
    city_display = serializers.CharField(source='get_city_display', read_only=True)
    # 自定义字段：厂家友好名称
    manufacturer_display = serializers.CharField(source='get_manufacturer_display', read_only=True)
    # 自定义字段：承包商友好名称
    contractor_display = serializers.CharField(source='get_contractor_display', read_only=True)
    # 自定义字段：投诉状态友好名称（0=无投诉，1=有投诉）
    has_complaint_display = serializers.CharField(source='get_has_complaint_display', read_only=True)
    # 自定义字段：一级场景友好名称
    scene_level1_display = serializers.CharField(source='get_scene_level1_display', read_only=True)
    # 自定义字段：室内外友好名称
    indoor_outdoor_display = serializers.CharField(source='get_indoor_outdoor_display', read_only=True)
    # 自定义字段：区域类型友好名称
    area_display = serializers.CharField(source='get_area_display', read_only=True)

    class Meta:
        model = NetworkSceneData
        fields = "__all__"
