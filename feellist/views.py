# 导入分页相关模块
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# 导入修改后的UserScore模型
from .models import UserScore, NetworkSceneData


# 序列化器：适配UserScore模型
class UserScoreSerializer(serializers.ModelSerializer):
    """
    序列化器：将UserScore模型数据转换为JSON格式
    作用：
    1. 模型数据转JSON，供前端解析
    2. 验证前端传入的新增/修改数据合法性
    3. 自定义字段（如netType_display）展示友好名称
    """
    # 自定义字段：展示网络类型的友好名称（基于模型的choices）
    netType_display = serializers.CharField(source='get_netType_display', read_only=True)
    # 自定义字段：一级场景友好名称
    sceneType_display = serializers.CharField(source='get_sceneType_display', read_only=True)

    class Meta:
        model = UserScore  # 关联的数据库模型
        fields = "__all__"  # 序列化模型所有字段


class UserScoreListView(APIView):
    """
    用户评分列表接口（支持多条件筛选 + 分页）
    - GET：按手机号/小区ID/网络类型筛选查询，支持分页
    - POST：新增单条用户评分数据
    """

    def get(self, request):
        """
        GET请求处理逻辑：
        1. 接收前端筛选参数 + 分页参数
        2. 执行条件筛选
        3. 分页处理查询结果
        4. 按统一格式返回数据（list+total）
        """
        """GET请求处理逻辑"""
        # ========== 新增：打印全量请求信息 ==========
        print("===== 后端接收到的完整请求信息 =====")
        # 1. 打印所有GET参数（URL参数）
        print("1. URL参数（request.GET）：", dict(request.GET))
        # 2. 打印请求体（GET请求默认空，若有值说明参数传错位置）
        # 临时修改：将二进制request.body转为字符串（避免Windows终端报错）
        print("2. 请求体（request.body）：", str(request.body))  # 仅改这一行，加str()转换
        # print("2. 请求体（request.body）：", request.body)
        # 3. 打印完整请求URL
        print("3. 完整请求URL：", request.build_absolute_uri())
        # 4. 打印请求方法
        print("4. 请求方法：", request.method)
        print("====================================\n")
        # ===================== 1. 获取并校验前端传入的参数 =====================
        # 筛选参数（强制去除首尾空格，避免空格导致筛选失效）
        phone = request.GET.get('phonenuber', '').strip()  # 手机号筛选（精准匹配）
        print("请求的手机号参数：", phone)
        # phone = "16679004215"  # 手机号筛选（精准匹配）
        cell_id = request.GET.get('cellId', '').strip()  # 小区ID筛选（数字）
        net_type = request.GET.get('netType', '').strip()  # 网络类型筛选（0/1/2/3/4）

        # 分页参数（前端默认传page=1，page_size=10，未传则使用默认值）
        page = request.GET.get('page', 1)  # 当前页码
        page_size = request.GET.get('page_size', 10)  # 每页条数

        # 调试日志：打印接收的参数（后端控制台查看）
        print("=" * 50)
        print(f"【后端】接收的手机号参数：{phone}（长度：{len(phone)}）")
        print(f"【后端】接收的小区ID参数：{cell_id}")
        print(f"【后端】接收的网络类型参数：{net_type}")
        print("=" * 50)

        # ===================== 2. 初始化并筛选查询集 =====================
        # 初始化查询集：查询UserScore表所有数据
        queryset = UserScore.objects.all().order_by('-id')  # 按ID倒序，最新数据在前

        # 标记是否有筛选条件（用于判断无数据时的提示逻辑）
        has_filter = False

        # 手机号筛选：仅当参数非空时执行筛选（精准匹配）
        if phone:
            queryset = queryset.filter(phonenuber=phone)
            has_filter = True
            print(f"【后端】手机号筛选后数据量：{queryset.count()}")
            # print(f"【后端】写死手机号筛选后数据量：{queryset.count()}")  # 打印筛选后数量

        # 小区ID筛选：先转换为数字，避免非数字参数报错
        if cell_id:
            try:
                cell_id_int = int(cell_id)  # 转换为整数
                queryset = queryset.filter(cellId=cell_id_int)
                has_filter = True
                print(f"【后端】小区ID筛选后数据量：{queryset.count()}")
            except ValueError:
                # 小区ID非数字时，返回400参数错误
                return Response({
                    "code": 400,
                    "msg": "小区ID必须是数字格式",
                    "list": [],  # 前端预期的列表字段
                    "total": 0  # 前端预期的总数字段
                }, status=status.HTTP_400_BAD_REQUEST)

        # 网络类型筛选：匹配choices的存储值（0/1/2/3/4）
        if net_type:
            queryset = queryset.filter(netType=net_type)
            has_filter = True
            print(f"【后端】网络类型筛选后数据量：{queryset.count()}")

        # ===================== 3. 分页处理 =====================
        # 初始化分页器：传入查询集 + 每页条数
        paginator = Paginator(queryset, page_size)

        try:
            # 转换页码为整数，避免非数字页码报错
            page_int = int(page)
            # 获取当前页的数据
            page_data = paginator.page(page_int)
        except PageNotAnInteger:
            # 页码非整数时，默认返回第1页
            page_data = paginator.page(1)
        except EmptyPage:
            # 页码超出范围时，返回空数据（无最后一页兜底）
            page_data = paginator.page(paginator.num_pages)

        # ===================== 4. 序列化 + 结果判断 =====================
        # 序列化当前页数据（many=True表示多条数据）
        serializer = UserScoreSerializer(page_data, many=True)

        # 总记录数（筛选后的总数）
        total = paginator.count

        # 调试日志：打印最终筛选结果
        print(f"【后端】筛选后总数据量：{total}")

        # 有筛选条件但无数据时，返回404提示
        if has_filter and total == 0:
            return Response({
                "code": 404,
                "msg": "查询的号码/数据不存在",
                "list": [],  # 前端接收的列表字段
                "total": 0  # 前端接收的总数字段
            }, status=status.HTTP_404_NOT_FOUND)

        # ===================== 5. 正常返回数据 =====================
        return Response({
            "code": 200,
            "msg": "查询成功",
            "list": serializer.data,  # 当前页数据列表（前端预期的字段名）
            "total": total  # 筛选后的总记录数（分页总条数）
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        POST请求处理逻辑：新增单条用户评分数据
        1. 接收前端传入的JSON数据
        2. 验证数据合法性
        3. 保存到数据库
        4. 返回新增后的数据
        """
        # 序列化前端传入的数据（验证+转换）
        serializer = UserScoreSerializer(data=request.data)

        # 验证数据合法性（如字段类型、长度、必填项等）
        if serializer.is_valid():
            # 数据合法，保存到数据库
            serializer.save()
            # 返回新增成功的响应（包含新增的数据）
            return Response({
                "code": 201,
                "msg": "数据新增成功",
                "list": [serializer.data],  # 保持list字段格式统一
                "total": 1
            }, status=status.HTTP_201_CREATED)

        # 数据验证失败，返回错误信息
        return Response({
            "code": 400,
            "msg": "数据新增失败",
            "error": serializer.errors,  # 具体的验证错误（如字段缺失、格式错误）
            "list": [],
            "total": 0
        }, status=status.HTTP_400_BAD_REQUEST)


class UserScoreDetailView(APIView):
    """
    用户评分详情接口：处理单条数据的查询/修改/删除
    - GET：查询单条数据（按ID）
    - PUT：修改单条数据（按ID）
    - DELETE：删除单条数据（按ID）
    """

    def get_object(self, pk):
        """
        通用方法：根据主键ID获取单条数据，不存在则返回404
        :param pk: 数据主键ID
        :return: UserScore实例 / 404响应
        """
        return get_object_or_404(UserScore, pk=pk)

    def get(self, request, pk):
        """
        GET请求：查询单条数据（按ID）
        :param pk: 数据主键ID
        """
        # 获取单条数据
        obj = self.get_object(pk)
        # 序列化数据
        serializer = UserScoreSerializer(obj)
        # 返回数据（保持list+total格式，适配前端统一解析逻辑）
        return Response({
            "code": 200,
            "msg": "查询成功",
            "list": [serializer.data],  # 单条数据包装为列表
            "total": 1
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        PUT请求：修改单条数据（按ID）
        :param pk: 数据主键ID
        """
        # 获取要修改的原始数据
        obj = self.get_object(pk)
        # 序列化前端传入的修改数据（partial=False表示全量更新，如需局部更新可设为True）
        serializer = UserScoreSerializer(obj, data=request.data)

        # 验证修改数据的合法性
        if serializer.is_valid():
            serializer.save()  # 保存修改后的数据
            return Response({
                "code": 200,
                "msg": "数据修改成功",
                "list": [serializer.data],  # 返回修改后的数据
                "total": 1
            }, status=status.HTTP_200_OK)

        # 验证失败，返回错误信息
        return Response({
            "code": 400,
            "msg": "数据修改失败",
            "error": serializer.errors,
            "list": [],
            "total": 0
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        DELETE请求：删除单条数据（按ID）
        :param pk: 数据主键ID
        """
        # 获取要删除的数据
        obj = self.get_object(pk)
        # 执行删除操作
        obj.delete()
        # 返回删除成功的响应
        return Response({
            "code": 204,
            "msg": "数据删除成功",
            "list": [],
            "total": 0
        }, status=status.HTTP_204_NO_CONTENT)


# ===================== NetworkSceneData 新增序列化器和接口 =====================
class NetworkSceneDataSerializer(serializers.ModelSerializer):
    """
    序列化器：NetworkSceneData模型专属
    特性：
    1. 序列化/反序列化模型所有字段
    2. 自定义枚举字段的友好名称展示（如has_complaint_display、indoor_outdoor_display等）
    3. 自动验证字段合法性（如经纬度范围、评分0-100等）
    """
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
    area_type_display = serializers.CharField(source='get_area_type_display', read_only=True)

    class Meta:
        model = NetworkSceneData
        fields = "__all__"  # 序列化所有字段（也可指定具体字段：fields = ['date', 'city', ...]）


class NetworkSceneDataListView(APIView):
    """
    小区场景数据列表接口（对齐UserScore逻辑：多条件筛选 + 分页 + 新增）
    - GET：按地市/小区ID/投诉状态/区域类型筛选，支持分页
    - POST：新增单条小区场景数据
    """

    def get(self, request):
        """
        GET请求：多条件筛选 + 分页查询
        筛选维度：地市、小区ID、投诉状态、区域类型、一级场景
        """
        # ========== 打印请求调试信息 ==========
        print("===== 小区场景数据接口 - 接收的请求信息 =====")
        print("1. URL参数：", dict(request.GET))
        print("2. 请求体：", str(request.body))
        print("3. 完整URL：", request.build_absolute_uri())
        print("4. 请求方法：", request.method)
        print("==========================================\n")

        # ===================== 1. 获取前端参数 =====================
        # 筛选参数（去空格，避免无效筛选）
        city = request.GET.get('city', '').strip()  # 地市筛选（模糊匹配）
        cell_id = request.GET.get('cell_id', '').strip()  # 小区ID（精准匹配）
        has_complaint = request.GET.get('has_complaint', '').strip()  # 投诉状态（0/1）
        area_type = request.GET.get('area_type', '').strip()  # 区域类型（rural/town/city/county）
        scene_level1 = request.GET.get('scene_level1', '').strip()  # 一级场景（居家/办公/出行）

        # 分页参数
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        # 调试日志
        print("=" * 60)
        print(f"【小区数据】地市：{city} | 小区ID：{cell_id} | 投诉状态：{has_complaint}")
        print(f"【小区数据】区域类型：{area_type} | 一级场景：{scene_level1}")
        print("=" * 60)

        # ===================== 2. 初始化查询集并筛选 =====================
        queryset = NetworkSceneData.objects.all().order_by('-id')  # 按ID倒序
        has_filter = False  # 标记是否有筛选条件

        # # 厂家筛选（0/1）
        # if contractor in ['0', '1']:
        #     queryset = queryset.filter(contractor=int(contractor))
        #     has_filter = True
        #     print(f"【小区数据】投诉状态筛选后数量：{queryset.count()}")

        # 地市筛选：模糊匹配（如输入"北京"能匹配"北京市朝阳区"）
        if city:
            queryset = queryset.filter(city__contains=city)
            has_filter = True
            print(f"【小区数据】地市筛选后数量：{queryset.count()}")

        # 小区ID筛选：转换为整数，避免非数字报错
        if cell_id:
            try:
                cell_id_int = int(cell_id)
                queryset = queryset.filter(cell_id=cell_id_int)
                has_filter = True
                print(f"【小区数据】小区ID筛选后数量：{queryset.count()}")
            except ValueError:
                return Response({
                    "code": 400,
                    "msg": "小区ID必须是数字格式",
                    "list": [],
                    "total": 0
                }, status=status.HTTP_400_BAD_REQUEST)

        # 投诉状态筛选（0/1）
        if has_complaint in ['0', '1']:
            queryset = queryset.filter(has_complaint=int(has_complaint))
            has_filter = True
            print(f"【小区数据】投诉状态筛选后数量：{queryset.count()}")

        # 区域类型筛选（匹配枚举值：rural/town/city/county）
        if area_type:
            queryset = queryset.filter(area_type=area_type)
            has_filter = True
            print(f"【小区数据】区域类型筛选后数量：{queryset.count()}")

        # 一级场景筛选（模糊匹配），中文改为精准匹配数字编码
        # if scene_level1:
        #     queryset = queryset.filter(scene_level1__contains=scene_level1)
        #     has_filter = True
        #     print(f"【小区数据】一级场景筛选后数量：{queryset.count()}")
        # 修复后代码
        if scene_level1:
            try:
                scene_level1_int = int(scene_level1)  # 转换为整数（防非数字）
                queryset = queryset.filter(scene_level1=scene_level1_int)  # 精准匹配（数字字段必须用=）
                has_filter = True
                print(f"【小区数据】一级场景筛选后数量：{queryset.count()}")
            except ValueError:
                return Response({
                    "code": 400,
                    "msg": "一级场景必须是数字格式（0-7）",
                    "list": [],
                    "total": 0
                }, status=status.HTTP_400_BAD_REQUEST)

        # ===================== 3. 分页处理 =====================
        paginator = Paginator(queryset, page_size)
        try:
            page_int = int(page)
            page_data = paginator.page(page_int)
        except PageNotAnInteger:
            page_data = paginator.page(1)
        except EmptyPage:
            page_data = paginator.page(paginator.num_pages)

        # ===================== 4. 序列化 + 响应 =====================
        serializer = NetworkSceneDataSerializer(page_data, many=True)
        total = paginator.count

        print(f"【小区数据】最终筛选后总数量：{total}")

        # 有筛选条件但无数据时返回404
        if has_filter and total == 0:
            return Response({
                "code": 404,
                "msg": "查询的小区场景数据不存在",
                "list": [],
                "total": 0
            }, status=status.HTTP_404_NOT_FOUND)

        # 正常返回
        return Response({
            "code": 200,
            "msg": "小区场景数据查询成功",
            "list": serializer.data,
            "total": total
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        POST请求：新增单条小区场景数据
        逻辑和UserScore对齐，自动验证字段合法性
        """
        serializer = NetworkSceneDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 201,
                "msg": "小区场景数据新增成功",
                "list": [serializer.data],
                "total": 1
            }, status=status.HTTP_201_CREATED)

        # 验证失败返回错误
        return Response({
            "code": 400,
            "msg": "小区场景数据新增失败",
            "error": serializer.errors,
            "list": [],
            "total": 0
        }, status=status.HTTP_400_BAD_REQUEST)


class NetworkSceneDataDetailView(APIView):
    """
    小区场景数据详情接口（单条CRUD）
    - GET：查询单条数据（按ID）
    - PUT：修改单条数据（按ID）
    - DELETE：删除单条数据（按ID）
    """

    def get_object(self, pk):
        """通用方法：按ID获取数据，不存在则404"""
        return get_object_or_404(NetworkSceneData, pk=pk)

    def get(self, request, pk):
        """查询单条小区场景数据"""
        obj = self.get_object(pk)
        serializer = NetworkSceneDataSerializer(obj)
        return Response({
            "code": 200,
            "msg": "小区场景数据查询成功",
            "list": [serializer.data],
            "total": 1
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """修改单条小区场景数据"""
        obj = self.get_object(pk)
        # partial=True 支持局部更新（可选，根据业务需求调整）
        serializer = NetworkSceneDataSerializer(obj, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 200,
                "msg": "小区场景数据修改成功",
                "list": [serializer.data],
                "total": 1
            }, status=status.HTTP_200_OK)

        return Response({
            "code": 400,
            "msg": "小区场景数据修改失败",
            "error": serializer.errors,
            "list": [],
            "total": 0
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """删除单条小区场景数据"""
        obj = self.get_object(pk)
        obj.delete()
        return Response({
            "code": 204,
            "msg": "小区场景数据删除成功",
            "list": [],
            "total": 0
        }, status=status.HTTP_204_NO_CONTENT)
