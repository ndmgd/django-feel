from django.db import models


# 用户字段组件：生成用户字段
def user_indicator_fields():
    """生成通用的流量戳字段"""
    return {
        "flu": models.FloatField(verbose_name="流量(MB)", null=True, blank=True, ),
        'MR_rate': models.FloatField(verbose_name="RSRP>=-110dBm占比", null=True, blank=True, ),
        'Ta_avg': models.FloatField(verbose_name="Ta平均值", null=True, blank=True, ),
        'MR_avg': models.FloatField(verbose_name="用户级平均RSRP", null=True, blank=True, ),
        'MR_overlap_coverage_rate': models.FloatField(verbose_name="用户级MR重叠覆盖率", null=True, blank=True),
        'RSRQ_avg': models.FloatField(verbose_name="用户级平均RSRQ", null=True, blank=True),
        'large_packet_rate_kbps': models.FloatField(verbose_name="用户级大包速率kbps", null=True, blank=True),
        'web_tcp_latency_ms': models.FloatField(verbose_name="用户级浏览网页TCP时延ms", null=True, blank=True),
        'im_tcp_latency_ms': models.FloatField(verbose_name="用户级即时通讯TCP时延ms", null=True, blank=True),
        'game_tcp_latency_ms': models.FloatField(verbose_name="用户级游戏时延（TCP时延）ms", null=True, blank=True),
        'video_tcp_latency_ms': models.FloatField(verbose_name="用户级视频TCP时延ms", null=True, blank=True),
        'call_setup_req_count': models.IntegerField(verbose_name="呼叫建立请求次数", null=True, blank=True),
        'call_link_success_count_excl_user': models.IntegerField(verbose_name="呼叫建链成功次数（去除用户原因）",
                                                                 null=True, blank=True),
        'call_link_success_rate_excl_user': models.FloatField(verbose_name="呼叫建链成功率（去除用户原因）", null=True,
                                                              blank=True),
        'MOS_avg': models.FloatField(verbose_name="平均MOS", null=True, blank=True),
        'MOS_ul_avg': models.FloatField(verbose_name="上行平均MOS", null=True, blank=True),
        'MOS_dl_avg': models.FloatField(verbose_name="下行平均MOS", null=True, blank=True),
        'ul_interrupt_rate': models.FloatField(verbose_name="用户级上行断续率", null=True, blank=True),
        'ul_one_way_audio_rate': models.FloatField(verbose_name="用户级上行单通率", null=True, blank=True),
    }
