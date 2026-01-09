from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from feellist.fileds.base_fileds import city_field, phone_field, net_type_field, score_field, CSB_field, scene_field, \
    time_fields, sent_time_field, manufacturer_field, contractor_field, complaint_field, coordinate_field, \
    indoor_outdoor_field, area_field
from feellist.fileds.cell_indicator_fileds import cell_indicator_fields
from feellist.fileds.meta import FieldComposeMeta
from feellist.fileds.user_indicator_fileds import user_indicator_fields


class UserScore_old(models.Model, metaclass=FieldComposeMeta):
    _compose_city = city_field
    _compose_phone = phone_field
    _compose_net_type = net_type_field
    _compose_score = lambda: score_field(field_name="cell_score", verbose_name="小区评分")
    _compose_csb = CSB_field
    _compose_scene = scene_field
    _compose_time = time_fields
    _compose_user_indicator = user_indicator_fields()

    class Meta:
        db_table = "user_score"
        verbose_name = "用户评分表"
        verbose_name_plural = "用户评分表"
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["cell_id"]),
            models.Index(fields=["scene_id"]),
        ]

    def __str__(self):
        return f"{self.city}-{self.phone_number}-{self.cell_score}"


class NetworkSceneData_old(models.Model, metaclass=FieldComposeMeta):
    """网络场景数据表（修正后）"""
    # 自有字段
    # 组合公共字段（解包）
    # -------------------------- 组合公共字段（按你的示例格式重写） --------------------------
    _compose_senttime = sent_time_field()
    _compose_city = city_field()  # 地市字段
    _compose_csb = CSB_field()  # ECI/小区ID字段
    _compose_score = score_field(field_name="cell_score", verbose_name="小区评分")  # 小区评分
    _compose_cell_indicator = cell_indicator_fields()
    # 自有字段
    cell_user_avg_score = models.FloatField(
        verbose_name="小区内用户均分",
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # 组合公共字段（修正拼写错误）
    _compose_manufacturer = manufacturer_field()  # 厂家字段
    _compose_contractor = contractor_field()  # 承建方字段
    _compose_complaint = complaint_field()  # 投诉字段
    _compose_coordinate = coordinate_field()  # 经纬度字段
    _compose_scene = scene_field()  # 场景字段
    _compose_indoor_outdoor = indoor_outdoor_field()  # 室内外字段
    _compose_area = area_field()  # 区域类型字段
    _compose_time = time_fields()  # 时间字段

    class Meta:
        db_table = "network_scene_data"
        verbose_name = "小区数据表"
        verbose_name_plural = "小区数据表"
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["cell_id"]),
            models.Index(fields=["scene_id"]),
            models.Index(fields=["city"]),
        ]

    def __str__(self):
        return f"{self.date}-{self.city}-{self.cell_id}"
