from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class UserScore(models.Model):
    """
    网络评分模型（对应前端表格字段）
    字段映射：前端prop → 模型字段名（保持一致，减少前后端适配成本）
    """
    # 城市：短文本，最多50字（如"北京市"、"上海市浦东新区"）
    city = models.CharField(
        max_length=50,
        verbose_name="城市",
        null=True,
        blank=True
    )

    # 用户号码：手机号，11位，加正则验证
    phonenuber = models.CharField(  # 注意：前端prop是phonenuber（疑似笔误，建议和前端确认是否为phonenumber）
        max_length=11,
        verbose_name="用户号码",
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message='请输入有效的11位手机号',
                code='invalid_phone'
            )
        ]
    )

    # 评分：浮点型，范围0-100（可根据业务调整）
    score = models.FloatField(
        verbose_name="评分",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="评分不能低于0"),
            MaxValueValidator(100, message="评分不能高于100")
        ]
    )

    # 网络类型：短文本（如"5G"、"4G"、"WiFi"）
    netType = models.IntegerField(  # 从 CharField 改为 IntegerField
        verbose_name="网络类型",
        null=True,
        blank=True,
        choices=[
            (0, "5G"),  # 第一个值改为数字（不再是字符串）
            (1, "4G"),
            (2, "WiFi"),
            (3, "宽带"),
            (4, "其他")
        ]
    )

    # 常驻小区评分：浮点型，范围0-100
    cellScore = models.FloatField(
        verbose_name="常驻小区评分",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="小区评分不能低于0"),
            MaxValueValidator(100, message="小区评分不能高于100")
        ]
    )

    # 小区名称：文本，最多100字（如"XX小区-南区"）
    cellName = models.CharField(
        max_length=100,
        verbose_name="小区名称",
        null=True,
        blank=True
    )

    # 小区ID：纯数字类型（BigIntegerField避免数值溢出，支持更大范围的数字ID）
    cellId = models.BigIntegerField(
        verbose_name="小区ID",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="小区ID不能为负数")  # 确保ID为非负整数
        ]
    )

    # 关联场景ID：字符型（场景ID通常为字符串格式）
    sceneId = models.CharField(
        max_length=50,
        verbose_name="关联场景ID",
        null=True,
        blank=True
    )

    # 场景名称：短文本（如"居家"、"办公"、"出行"）
    sceneName = models.CharField(
        max_length=50,
        verbose_name="场景名称",
        null=True,
        blank=True
    )

    # 一级场景类型：短文本（如"居家"、"办公"、"出行"）
    sceneType = models.CharField(
        max_length=50,
        verbose_name="一级场景类型",
        null=True,
        blank=True
    )

    # 二级场景类型：短文本（如"居家-客厅"、"办公-会议室"）
    sceneSubType = models.CharField(
        max_length=100,
        verbose_name="二级场景类型",
        null=True,
        blank=True
    )

    # 自动维护创建/更新时间（可选，建议添加，便于数据追溯）
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_score"  # 数据库表名（小写+下划线，符合规范）
        verbose_name = "用户评分表"
        verbose_name_plural = "用户评分表"  # 复数名和单数名一致，避免后台显示"网络评分表s"
        indexes = [
            # 常用查询字段加索引，提升查询效率
            models.Index(fields=["phonenuber"]),  # 按手机号查询
            models.Index(fields=["cellId"]),  # 按小区ID查询
            models.Index(fields=["sceneId"]),  # 按场景ID查询
        ]

    def __str__(self):
        """后台显示友好名称，便于调试"""
        return f"{self.city}-{self.phonenuber}-{self.score}"
