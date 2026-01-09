from django.db import models


def cell_indicator_fields():
    return {
        'volte_connect_rate': models.FloatField(verbose_name="VOLTE接通率", null=True, blank=True),
        'lte_service_drop_rate_qci1': models.FloatField(verbose_name="LTE业务掉线率(QCI1)", null=True, blank=True),
        'qci1_ul_pdcp_sdu_loss_rate': models.FloatField(verbose_name="QCI1的上行PDCP SDU丢包率", null=True, blank=True),
        'qci1_dl_pdcp_sdu_loss_rate': models.FloatField(verbose_name="QCI1的下行PDCP SDU丢包率", null=True, blank=True),
        'cqi_good_rate': models.FloatField(verbose_name="CQI优良率", null=True, blank=True),
        'dl_prb_utilization_mean': models.FloatField(verbose_name="下行PRB利用率_Mean", null=True, blank=True),
        'carrier_avg_noise_interference_health': models.FloatField(verbose_name="载波平均噪声干扰-健康度", null=True,
                                                                   blank=True),
        'total_sample_points_sum': models.IntegerField(verbose_name="总采样点数_Sum", null=True, blank=True),
        'overlap_coverage_sample_points_sum': models.IntegerField(verbose_name="重叠覆盖采样点数_Sum", null=True,
                                                                  blank=True),
        'overlap_coverage_ratio': models.FloatField(verbose_name="重叠覆盖比例", null=True, blank=True),
        'mro_rsrp_ge_110_sample_points_sum': models.IntegerField(verbose_name="MRO-RSRP≥-110采样点数_Sum", null=True,
                                                                 blank=True),
        'total_sample_point_sum': models.IntegerField(verbose_name="总采样点_Sum", null=True, blank=True),
        'rsrp_ge_110_ratio': models.FloatField(verbose_name="RSRP>=-110比例", null=True, blank=True),
        'total_sample_points_mod3_sum': models.IntegerField(verbose_name="总采样点数-mod3_Sum", null=True, blank=True),
        'mod3_interference_sample_points_sum': models.IntegerField(verbose_name="mod3干扰采样点数_Sum", null=True,
                                                                   blank=True),
        'mod3_interference_ratio': models.FloatField(verbose_name="MOD3干扰比例", null=True, blank=True),
    }
