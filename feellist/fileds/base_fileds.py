from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from feellist.common.constants import (
    CITY_CHOICES, SCENE_LEVEL1_CHOICES, NET_TYPE_CHOICES, MANUFACTURER_CHOICES, INDOOR_OUTDOOR_CHOICES, AREA_CHOICES,
    COMPLAINT_STATUS_CHOICES, CONTRACTOR_CHOICES
)


# 时间字段组件：生成创建/更新时间字段
def time_fields():
    """生成通用的时间戳字段"""
    return {
        "create_time": models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
        "update_time": models.DateTimeField(auto_now=True, verbose_name="更新时间"),
    }


# 发送时间字段组件：生成发送时间字段
def sent_time_field():
    """生成通用的发送时间字段"""
    return {
        "date": models.DateTimeField(verbose_name="日期", null=True, blank=True),
    }


# 地市字段组件：生成地市相关字段
def city_field():
    """生成通用的地市字段"""
    return {
        "city": models.IntegerField(
            verbose_name="地市",
            null=True,
            blank=True,
            choices=CITY_CHOICES
        )
    }


# 场景字段组件：生成场景相关字段
def scene_field():
    """生成通用的场景字段"""
    return {
        'scene_id': models.CharField(max_length=50, verbose_name="关联场景ID", null=True, blank=True),
        'sceneName': models.CharField(max_length=50, verbose_name="场景名称", null=True, blank=True),
        'scene_level1': models.IntegerField(verbose_name="一级场景", null=True, blank=True,
                                            choices=SCENE_LEVEL1_CHOICES),
        'scene_level2': models.CharField(max_length=100, verbose_name="二级场景", null=True, blank=True)
    }


# 网络类型字段组件：生成网络类型字段
def net_type_field():
    """生成网络类型字段"""
    return {
        'net_type': models.IntegerField(verbose_name="网络类型", null=True, blank=True, choices=NET_TYPE_CHOICES)
    }


# 基站字段组件：生成基站字段
def CSB_field():
    """生成通用的ECI字段"""
    return {
        'cellName': models.CharField(max_length=100, verbose_name="小区名称", null=True, blank=True),
        "eci": models.BigIntegerField(verbose_name="ECI", null=True, blank=True,
                                      validators=[MinValueValidator(0, message="基站ID不能为负数")]),
        'cell_id': models.BigIntegerField(verbose_name="cellID", null=True, blank=True,
                                          validators=[MinValueValidator(0, message="小区ID不能为负数")])
    }


# 厂家字段组件：生成厂商字段（修正函数名拼写错误：manmanufacturer → manufacturer）
def manufacturer_field():
    """生成厂商字段"""
    return {
        'manufacturer': models.IntegerField(  # IntegerField无需max_length，删除该参数
            verbose_name="厂家",
            null=True,
            blank=True,
            choices=MANUFACTURER_CHOICES
        )
    }


# 经纬度字段组件：生成经纬度字段（修正校验器：MinValueValidator重复 → 补充MaxValueValidator）
def coordinate_field():
    """生成经纬度字段"""
    return {
        "longitude": models.FloatField(
            verbose_name="经度",
            null=True,
            blank=True,
            validators=[MinValueValidator(-180), MaxValueValidator(180)]  # 修正：经度范围-180~180
        ),
        "latitude": models.FloatField(
            verbose_name="纬度",
            null=True,
            blank=True,
            validators=[MinValueValidator(-90), MaxValueValidator(90)]  # 修正：纬度范围-90~90
        ),
    }


# 室内外字段组件：生成室内外字段
def indoor_outdoor_field():
    """生成室内外字段"""
    return {
        'indoor_outdoor': models.IntegerField(verbose_name="室内外", null=True, blank=True,
                                              choices=INDOOR_OUTDOOR_CHOICES)
    }


# 区域字段组件：生成区域字段（修正：IntegerField的choices值不能是字符串 → 改为数字）
def area_field():
    """生成区域字段"""
    return {
        'area': models.IntegerField(
            verbose_name="区域",
            null=True,
            blank=True,
            choices=AREA_CHOICES  # 修正：去掉引号，用数字
        )
    }


# 电话字段组件：生成手机号码字段
def phone_field():
    """生成手机号码字段"""
    return {
        'phone_number': models.CharField(
            max_length=11,
            verbose_name="用户号码",
            null=True,
            blank=True,
            validators=[RegexValidator(regex=r'^1[3-9]\d{9}$', message='请输入有效的11位手机号', code='invalid_phone')]
        )
    }


# 评分字段组件：生成带校验的评分字段（修正校验器：MinValueValidator重复 → 补充MaxValueValidator）
def score_field(field_name="score", verbose_name="评分"):
    """生成通用的评分字段（支持自定义字段名和描述）"""
    return {
        field_name: models.FloatField(
            verbose_name=verbose_name,
            null=True,
            blank=True,
            validators=[MinValueValidator(0), MaxValueValidator(100)]  # 修正：0~100范围
        ),
    }


# 投诉字段组件：生成投诉相关字段
def complaint_field():
    """生成投诉相关字段"""
    return {
        'has_complaint': models.IntegerField(verbose_name="是否存在关联投诉工单", null=True, blank=True,
                                             choices=COMPLAINT_STATUS_CHOICES)
    }


# 承建方字段组件：生成承建方相关字段（修正函数名拼写错误：contractor_filed → contractor_field）
def contractor_field():
    """生成 Contractor 字段（修正：IntegerField而非CharField，因为choices值是数字）"""
    return {
        'contractor': models.IntegerField(
            verbose_name="承建方",
            null=True,
            blank=True,
            choices=CONTRACTOR_CHOICES
        )
    }
