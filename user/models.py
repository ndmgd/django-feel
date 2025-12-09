from django.db import models

# 新增：导入Django抽象用户类
from django.contrib.auth.models import AbstractUser


class SysUser(AbstractUser):
    # 1. 删掉手动定义的 username/password（AbstractUser 已内置，且自动处理密码哈希）
    # 保留你的自定义字段（字段名和类型不变，仅调整冗余项）
    avatar = models.CharField(max_length=255, null=True, verbose_name="用户头像")
    email = models.CharField(max_length=100, null=True, verbose_name="用户邮箱")
    phonenumber = models.CharField(max_length=11, null=True, verbose_name="手机号码")
    login_date = models.DateField(null=True, verbose_name="最后登录时间")
    status = models.IntegerField(null=True, verbose_name="帐号状态（0正常 1停用）")
    create_time = models.DateField(null=True, verbose_name="创建时间")
    update_time = models.DateField(null=True, verbose_name="更新时间")
    remark = models.CharField(max_length=500, null=True, verbose_name="备注")

    class Meta:
        db_table = "sys_user"  # 保持自定义表名不变
        verbose_name = "系统用户"
        verbose_name_plural = "系统用户"
