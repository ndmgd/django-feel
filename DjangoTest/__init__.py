# django-feel/__init__.py
import pymysql

# 1. 让 pymysql 模拟 MySQLdb
pymysql.install_as_MySQLdb()

# 2. 修改 pymysql 暴露的版本号，满足 Django 的版本校验
pymysql.version_info = (2, 2, 5, "final", 0)  # 伪装成 mysqlclient 2.2.5
pymysql.__version__ = "2.2.5"
