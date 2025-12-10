from django.http import JsonResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from user.models import SysUser


# 登录接口
class LoginView(APIView):
    def post(self, request):
        # 1. 获取POST请求的参数（前端传的是JSON的话用request.data，表单用request.POST）
        # 注意：如果前端是通过URL参数传参，才用request.query_params；POST建议用request.data
        username = request.data.get("userName")  # 优先用request.data（对应POST的请求体）
        password = request.data.get("passWord")

        # 打印请求参数（方便排查）
        print(f"登录请求参数：用户名={username}，密码={password}")

        try:
            # 2. 查询用户（只按用户名查，密码后续用check_password校验）
            user = SysUser.objects.get(username=username)
            print(f"数据库中{username}的密码哈希：{user.password}")

            # 3. 校验密码（必须用check_password，因为密码是哈希存储的，不能直接==比较）
            if not user.check_password(password):
                return Response({"code": 400, "msg": "密码错误"}, status=400)

            # 4. 生成JWT令牌（和JwtTestView逻辑一致）
            token = AccessToken.for_user(user)
            return Response({"code": 200, "token": str(token), "info": "登录成功"})

        except SysUser.DoesNotExist:
            # 用户不存在的异常
            return Response({"code": 404, "msg": "用户名不存在"}, status=404)
        except Exception as e:
            # 其他未知异常
            print(f"登录异常：{e}")
            return Response({"code": 500, "msg": "登录失败，请稍后重试"}, status=500)


# 测试GET接口
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


# 测试JWT接口
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
