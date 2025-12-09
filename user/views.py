from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from user.models import SysUser


class TestView(View):
    def get(self, request):
        userList_obj = SysUser.objects.all()
        userList_dic = userList_obj.values()  # 转成字典
        userList = list(userList_dic)  # 把外层的容器转成列表
        return JsonResponse(
            {
                "code": 200,
                "msg": "GET请求成功（跨域测试）",
                "data": userList,
            }
        )


# 修正后的 JwtTestView
class JwtTestView(APIView):
    def get(self, request):
        # 打印实际请求的参数（方便排查）
        print(f"实际请求参数：{request.query_params}")
        try:
            # 1. 查询自定义用户表
            user = SysUser.objects.get(username="python222")
            print(f"数据库中python222的密码哈希：{user.password}")
            print(f"数据库中python222的密码哈希：{user.check_password("123456")}")
            # 2. 校验密码（必须用 check_password，因为密码是哈希存储的）
            if not user.check_password("123456"):
                return Response({"code": 400, "msg": "密码错误"}, status=400)

            # 3. 生成JWT令牌（现在支持自定义用户模型）
            token = AccessToken.for_user(user)
            return Response({"code": 200, "token": str(token)})

        except SysUser.DoesNotExist:
            return Response({"code": 404, "msg": "用户不存在"}, status=404)
