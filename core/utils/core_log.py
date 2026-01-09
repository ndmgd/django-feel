"""
项目级通用日志工具：所有APP的接口都能用这个打印日志
新手必看：
- 日志会自动美化，带时间、级别
- 调试时看控制台，能清楚看到请求参数和流程
"""
import logging

import coloredlogs
from django.http import HttpRequest

# 配置日志
logger = logging.getLogger("network_optimization")  # 项目名作为日志名

# 初始化彩色日志
coloredlogs.install(
    level="INFO",
    logger=logger,
    fmt="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def log_request(request: HttpRequest):
    """
    打印请求日志
    :param request: Django/DRF的请求对象
    """
    logger.info("===== 接收到新请求 =====")
    logger.info(f"请求路径: {request.path}")
    logger.info(f"请求方法: {request.method}")
    logger.info(f"客户端IP: {request.META.get('REMOTE_ADDR')}")
    logger.info(f"URL参数: {dict(request.GET)}")
    if request.body:
        logger.info(f"请求体: {request.body.decode('utf-8')}")
    logger.info("=======================\n")


def log_response(data: dict, status_code: int):
    """
    打印响应日志
    :param data: 响应数据
    :param status_code: 响应状态码
    """
    logger.info("===== 发送响应数据 =====")
    logger.info(f"状态码: {status_code}")
    logger.info(f"响应数据: {data}")
    logger.info("=======================\n")
