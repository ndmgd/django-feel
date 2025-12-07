from rest_framework.decorators import api_view
from rest_framework.response import Response

# 测试GET接口
@api_view(['GET'])
def test_get(request):
    """
    跨域测试GET接口
    参数：无（或可通过query_params接收前端参数）
    返回：简单的JSON数据
    """
    # 获取前端传递的参数（可选）
    name = request.query_params.get('name', '匿名用户')
    return Response({
        'code': 200,
        'msg': 'GET请求成功（跨域测试）',
        'data': f'你好，{name}！这是Django返回的GET数据'
    })

# 测试POST接口
@api_view(['POST'])
def test_post(request):
    """
    跨域测试POST接口
    参数：从request.data接收JSON格式参数
    返回：包含前端参数的JSON数据
    """
    # 获取前端POST的JSON数据
    username = request.data.get('username', '')
    age = request.data.get('age', 0)
    return Response({
        'code': 200,
        'msg': 'POST请求成功（跨域测试）',
        'data': {
            'username': username,
            'age': age,
            'tip': '这是Django返回的POST数据'
        }
    })