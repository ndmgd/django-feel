"""
feellist APP的视图：调用服务层，处理请求和响应
新手必看：
- 继承DRF的APIView，复用core的通用工具
- 只需要指定服务、序列化器、参数映射，不用写重复代码
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants.core_constants import (
    HTTP_SUCCESS, HTTP_CREATED, HTTP_NO_CONTENT,
    MSG_QUERY_SUCCESS, MSG_CREATE_SUCCESS, MSG_UPDATE_SUCCESS, MSG_DELETE_SUCCESS
)
from core.permissions.core_permissions import AllowAny
from core.utils.core_filters import clean_request_params
from core.utils.core_log import log_request, log_response


class BaseListView(APIView):
    """
    列表视图基类：支持GET（筛选+分页）、POST（新增）
    子类需要指定：
    1. service: 业务服务实例
    2. serializer_class: 序列化器类
    3. filter_mapping: 参数映射字典（可选）
    4. permission_classes: 权限类（可选，默认允许匿名访问）
    """
    service = None
    serializer_class = None
    filter_mapping = {}
    permission_classes = [AllowAny]

    def get(self, request):
        """GET请求：获取列表数据"""
        # 1. 打印请求日志
        log_request(request)
        # 2. 清洗请求参数
        filters = clean_request_params(request.GET, self.filter_mapping)
        # 3. 获取分页参数
        page = request.GET.get("page")
        page_size = request.GET.get("page_size")
        # 4. 调用服务层获取数据
        data_list, total, has_filter = self.service.get_list(filters, page, page_size)
        # 5. 序列化数据
        serializer = self.serializer_class(data_list, many=True)
        # 6. 构造响应数据
        response_data = {
            "code": HTTP_SUCCESS,
            "msg": MSG_QUERY_SUCCESS,
            "list": serializer.data,
            "total": total
        }
        # 7. 打印响应日志
        log_response(response_data, HTTP_SUCCESS)
        # 8. 返回响应
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        """POST请求：新增数据"""
        log_request(request)
        # 1. 数据验证
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 2. 调用服务层新增数据
        obj = self.service.create(serializer.validated_data)
        # 3. 序列化新增的数据
        res_serializer = self.serializer_class(obj)
        # 4. 构造响应
        response_data = {
            "code": HTTP_CREATED,
            "msg": MSG_CREATE_SUCCESS,
            "data": res_serializer.data
        }
        log_response(response_data, HTTP_CREATED)
        return Response(response_data, status=status.HTTP_201_CREATED)


class BaseDetailView(APIView):
    """
    详情视图基类：支持GET（查单条）、PUT（改）、DELETE（删）
    """
    service = None
    serializer_class = None
    permission_classes = [AllowAny]

    def get(self, request, pk):
        """GET请求：获取单条数据"""
        log_request(request)
        # 1. 调用服务层获取数据
        obj = self.service.get_detail(pk)
        # 2. 序列化数据
        serializer = self.serializer_class(obj)
        # 3. 构造响应
        response_data = {
            "code": HTTP_SUCCESS,
            "msg": MSG_QUERY_SUCCESS,
            "data": serializer.data
        }
        log_response(response_data, HTTP_SUCCESS)
        return Response(response_data)

    def put(self, request, pk):
        """PUT请求：修改数据"""
        log_request(request)
        # 1. 数据验证
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 2. 调用服务层修改数据
        obj = self.service.update(pk, serializer.validated_data)
        # 3. 序列化修改后的数据
        res_serializer = self.serializer_class(obj)
        # 4. 构造响应
        response_data = {
            "code": HTTP_SUCCESS,
            "msg": MSG_UPDATE_SUCCESS,
            "data": res_serializer.data
        }
        log_response(response_data, HTTP_SUCCESS)
        return Response(response_data)

    def delete(self, request, pk):
        """DELETE请求：删除数据"""
        log_request(request)
        # 1. 调用服务层删除数据
        self.service.delete(pk)
        # 2. 构造响应
        response_data = {
            "code": HTTP_NO_CONTENT,
            "msg": MSG_DELETE_SUCCESS
        }
        log_response(response_data, HTTP_NO_CONTENT)
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


# ==================== 业务视图 ====================
from feellist.services.user_score import UserScoreService
from feellist.services.network_scene import NetworkSceneDataService
from feellist.serializers import UserScoreSerializer, NetworkSceneDataSerializer


class UserScoreListView(BaseListView):
    """用户评分列表视图"""
    service = UserScoreService()
    serializer_class = UserScoreSerializer
    filter_mapping = {
        "phonenuber": "phone_number",  # 前端可能传错的参数名
        "cellId": "cell_id",
        "netType": "net_type"
    }


class UserScoreDetailView(BaseDetailView):
    """用户评分详情视图"""
    service = UserScoreService()
    serializer_class = UserScoreSerializer


class NetworkSceneDataListView(BaseListView):
    """小区场景数据列表视图"""
    service = NetworkSceneDataService()
    serializer_class = NetworkSceneDataSerializer
    filter_mapping = {
        "areaType": "area",
        "sceneLevel1": "scene_level1"
    }


class NetworkSceneDataDetailView(BaseDetailView):
    """小区场景数据详情视图"""
    service = NetworkSceneDataService()
    serializer_class = NetworkSceneDataSerializer
