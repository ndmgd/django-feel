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

# 新增的第二个 Model 类（对应你提供的表格字段）
class NetworkSceneData(models.Model):
    """
    网络场景数据表（对应前端新表格字段）
    字段映射：前端表格列 → 模型字段名（按表格字段命名，便于前后端对接）
    """
    # 日期：日期类型（存储年月日，如2025-12-27）
    date = models.DateField(
        verbose_name="日期",
        null=True,
        blank=True
    )

    # 地市：短文本，最多50字（如"北京市"、"广东省深圳市"）
    city = models.CharField(
        max_length=50,
        verbose_name="地市",
        null=True,
        blank=True
    )

    # 基站ID：大整数类型（支持超大数字ID，避免溢出），非负
    base_station_id = models.BigIntegerField(
        verbose_name="基站ID",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="基站ID不能为负数")  # 确保ID是非负整数
        ]
    )

    # 小区ID：大整数类型，非负（和UserScore的cellId字段类型保持一致）
    cell_id = models.BigIntegerField(
        verbose_name="小区ID",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="小区ID不能为负数")
        ]
    )

    # 小区级评分：浮点型，范围0-100（和UserScore的score字段校验规则一致）
    cell_score = models.FloatField(
        verbose_name="小区级评分",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="小区级评分不能低于0"),
            MaxValueValidator(100, message="小区级评分不能高于100")
        ]
    )

    # 小区内用户均分：浮点型，范围0-100（反映小区用户评分均值）
    cell_user_avg_score = models.FloatField(
        verbose_name="小区内用户均分",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="小区内用户均分不能低于0"),
            MaxValueValidator(100, message="小区内用户均分不能高于100")
        ]
    )

    # 厂家：短文本，最多50字（如"华为"、"中兴"、"爱立信"）
    manufacturer = models.CharField(
        max_length=50,
        verbose_name="厂家",
        null=True,
        blank=True
    )

    # 承建方：短文本，最多100字（如"中国通信建设集团"、"华为技术服务有限公司"）
    contractor = models.CharField(
        max_length=100,
        verbose_name="承建方",
        null=True,
        blank=True
    )

    # 是否存在关联投诉工单：整数枚举（0=无投诉，1=有投诉）
    has_complaint = models.IntegerField(
        verbose_name="是否存在关联投诉工单",
        null=True,
        blank=True,
        choices=[
            (0, "无投诉"),  # 数据库存储0，后台/admin显示"无投诉"
            (1, "有投诉")  # 数据库存储1，后台/admin显示"有投诉"
        ]
    )

    # 经度：浮点型（存储地理经度，如116.403874）
    longitude = models.FloatField(
        verbose_name="经度",
        null=True,
        blank=True
    )

    # 纬度：浮点型（存储地理纬度，如39.914885）
    latitude = models.FloatField(
        verbose_name="纬度",
        null=True,
        blank=True
    )

    # 指标：短文本，最多50字（如"下载速率"、"上传速率"、"时延"）
    indicator = models.CharField(
        max_length=50,
        verbose_name="指标",
        null=True,
        blank=True
    )


    # 关联场景ID：字符型，最多50字（和UserScore的sceneId字段类型保持一致）
    scene_id = models.CharField(
        max_length=50,
        verbose_name="关联场景ID",
        null=True,
        blank=True
    )

    # 一级场景：短文本，最多50字（如"居家"、"办公"、"出行"）
    scene_level1 = models.CharField(
        max_length=50,
        verbose_name="一级场景",
        null=True,
        blank=True
    )

    # 二级场景：短文本，最多100字（如"居家-客厅"、"办公-会议室"）
    scene_level2 = models.CharField(
        max_length=100,
        verbose_name="二级场景",
        null=True,
        blank=True
    )

    # 场景名称：短文本，最多100字（场景全称，如"居家网络使用场景"）
    scene_name = models.CharField(
        max_length=100,
        verbose_name="场景名称",
        null=True,
        blank=True
    )

    # 室内室外：短文本，枚举约束（仅允许"室内"/"室外"）
    indoor_outdoor = models.CharField(
        max_length=10,
        verbose_name="室内室外",
        null=True,
        blank=True,
        choices=[  # 枚举值：(数据库存储值, 后台显示名称)
            ("indoor", "室内"),
            ("outdoor", "室外")
        ]
    )

    # 农村乡镇/城市县城：短文本，枚举约束（限定可选值）
    area_type = models.CharField(
        max_length=20,
        verbose_name="农村乡镇/城市县城",
        null=True,
        blank=True,
        choices=[
            ("rural", "农村"),
            ("town", "乡镇"),
            ("city", "城市"),
            ("county", "县城")
        ]
    )

    # 自动维护创建时间（数据入库时自动记录，不可修改）
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 自动维护更新时间（数据每次保存时自动更新）
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "network_scene_data"  # 数据库表名（小写+下划线，符合Django规范）
        verbose_name = "小区数据表"  # 后台显示的单表名称
        verbose_name_plural = "小区数据表"  # 后台显示的多表名称（避免自动加s）
        indexes = [
            # 常用查询字段加索引，提升查询效率
            models.Index(fields=["date"]),        # 按日期查询
            models.Index(fields=["cell_id"]),     # 按小区ID查询
            models.Index(fields=["scene_id"]),    # 按场景ID查询
            models.Index(fields=["city"]),        # 按地市查询
        ]

    def __str__(self):
        """Django后台/admin显示该条数据的友好名称，便于调试和查看"""
        return f"{self.date}-{self.city}-{self.cell_id}"
