from django.db import models


def complaint_fields():
    return {
        # ===================== 工单基础标识字段 =====================
        'work_order_no': models.CharField(verbose_name="工单号", max_length=64, null=True, blank=True),
        'service_flow_no': models.CharField(verbose_name="客服流水号", max_length=64, null=True, blank=True),
        'main_work_order_flow_no': models.CharField(verbose_name="主工单流水号", max_length=64, null=True, blank=True),
        'gis_complaint_flow_no': models.CharField(verbose_name="GIS投诉流水号", max_length=64, null=True, blank=True),

        # ===================== 用户及受理信息字段 =====================
        'report_phone': models.CharField(verbose_name="受理号码", max_length=20, null=True, blank=True),
        'report_path': models.CharField(verbose_name="受理路径", max_length=64, null=True, blank=True),
        'report_channel': models.CharField(verbose_name="受理渠道", max_length=32, null=True, blank=True),
        'user_package': models.CharField(verbose_name="用户套餐", max_length=64, null=True, blank=True),
        'customer_level': models.CharField(verbose_name="客户级别", max_length=16, null=True, blank=True),
        'area': models.CharField(verbose_name="区域", max_length=64, null=True, blank=True),

        # ===================== 投诉核心信息字段 =====================
        'complaint_content': models.TextField(verbose_name="投诉内容", null=True, blank=True),
        'complaint_address': models.CharField(verbose_name="投诉地址", max_length=255, null=True, blank=True),
        'complaint_detail': models.TextField(verbose_name="投诉详单", null=True, blank=True),
        'complaint_env': models.CharField(verbose_name="投诉点环境", max_length=128, null=True, blank=True),
        'longitude': models.FloatField(verbose_name="经度", null=True, blank=True),
        'latitude': models.FloatField(verbose_name="纬度", null=True, blank=True),

        # ===================== 处理回复信息字段 =====================
        'reply_service_content': models.TextField(verbose_name="回复客服内容", null=True, blank=True),
        'final_process_result': models.CharField(verbose_name="最终处理结果", max_length=255, null=True, blank=True),
        'work_order_qualification': models.CharField(verbose_name="工单定性", max_length=64, null=True, blank=True),
        'problem_responsibility': models.CharField(verbose_name="问题责任归属", max_length=64, null=True, blank=True),
        'professional_type': models.CharField(verbose_name="专业", max_length=32, null=True, blank=True),
        'network_type': models.CharField(verbose_name="网络类型", max_length=16, null=True, blank=True),
        'network_field': models.CharField(verbose_name="网络字段", max_length=64, null=True, blank=True),
        'business_category': models.CharField(verbose_name="业务类别", max_length=32, null=True, blank=True),
        'problem_solve_conclusion': models.CharField(verbose_name="问题解决结论", max_length=64, null=True, blank=True),

        # ===================== 工单流程管理字段 =====================
        'management_scope': models.CharField(verbose_name="管理范围", max_length=64, null=True, blank=True),
        'current_link': models.CharField(verbose_name="当前环节", max_length=32, null=True, blank=True),
        'work_order_status': models.CharField(verbose_name="工单状态", max_length=16, null=True, blank=True),
        'complaint_upgrade': models.CharField(verbose_name="投诉升级", max_length=8, null=True, blank=True),
        'work_order_points': models.IntegerField(verbose_name="工单积分", null=True, blank=True),
        'repeat_times': models.IntegerField(verbose_name="重复次数", null=True, blank=True),
        'is_cancel_redo': models.CharField(verbose_name="是否撤单重派", max_length=8, null=True, blank=True),
        'complaint_level': models.CharField(verbose_name="投诉等级", max_length=16, null=True, blank=True),
        'current_processor': models.CharField(verbose_name="当前处理人", max_length=32, null=True, blank=True),

        # ===================== 时间节点字段 =====================
        'system_receive_time': models.DateTimeField(verbose_name="系统接单时", null=True, blank=True),
        'service_reply_require_time': models.DateTimeField(verbose_name="客服要求回复时间", null=True, blank=True),
        'preliminary_reply_time': models.DateTimeField(verbose_name="初步回复时间", null=True, blank=True),
        'preliminary_reply_content': models.TextField(verbose_name="初步回复内容", null=True, blank=True),
        'solve_reply_time': models.DateTimeField(verbose_name="解决回复时间", null=True, blank=True),
        'solve_reply_content': models.TextField(verbose_name="解决回复内容", null=True, blank=True),
        'is_overtime': models.CharField(verbose_name="是否超时", max_length=8, null=True, blank=True),

        # ===================== 责任及处理执行字段 =====================
        'responsible_department': models.CharField(verbose_name="责任部门", max_length=64, null=True, blank=True),
        'is_on_site_process': models.CharField(verbose_name="是否现场处理", max_length=8, null=True, blank=True),
        'is_user_on_site': models.CharField(verbose_name="用户是否在现场", max_length=8, null=True, blank=True),
        'longitude_latitude_source': models.CharField(verbose_name="经纬度来源", max_length=32, null=True, blank=True),
        'tag': models.CharField(verbose_name="标签", max_length=128, null=True, blank=True),
        'confirmed_longitude': models.FloatField(verbose_name="确认经度", null=True, blank=True),
        'confirmed_latitude': models.FloatField(verbose_name="确认纬度", null=True, blank=True),
        'problem_category': models.CharField(verbose_name="问题类别", max_length=64, null=True, blank=True),
        'administrative_scene': models.CharField(verbose_name="行政场景", max_length=64, null=True, blank=True),
        'complaint_scene': models.CharField(verbose_name="投诉场景", max_length=64, null=True, blank=True),
        'problem_area': models.CharField(verbose_name="问题区域", max_length=64, null=True, blank=True),
        'is_solved': models.CharField(verbose_name="是否解决", max_length=8, null=True, blank=True),
        'qualification_category': models.CharField(verbose_name="定性类别", max_length=64, null=True, blank=True),
        'final_problem_qualification': models.CharField(verbose_name="最终问题定性", max_length=128, null=True,
                                                        blank=True),
        'final_problem_qualification_supp1': models.CharField(verbose_name="最终问题定性补充一", max_length=128,
                                                              null=True, blank=True),
        'final_problem_qualification_supp2': models.CharField(verbose_name="最终问题定性补充二", max_length=128,
                                                              null=True, blank=True),
        'process_type': models.CharField(verbose_name="处理类型", max_length=32, null=True, blank=True),
        'is_tracked': models.CharField(verbose_name="是否跟踪", max_length=8, null=True, blank=True),
        'is_filed': models.CharField(verbose_name="是否归档", max_length=8, null=True, blank=True),

        # ===================== 投诉形式及附件字段 =====================
        'is_voice_complaint': models.CharField(verbose_name="是否语音投诉", max_length=8, null=True, blank=True),
        'is_upload_attachment': models.CharField(verbose_name="是否上传附件", max_length=8, null=True, blank=True),

        # ===================== 事态及客户反馈字段 =====================
        'situation_trend': models.CharField(verbose_name="事态发展倾向", max_length=32, null=True, blank=True),
        'is_high_compensation': models.CharField(verbose_name="是否高额赔偿", max_length=8, null=True, blank=True),
        'is_upgrade_tendency': models.CharField(verbose_name="是否升级倾向", max_length=8, null=True, blank=True),
        'is_media_exposure_tendency': models.CharField(verbose_name="是否媒体曝光倾向", max_length=8, null=True,
                                                       blank=True),
        'customer_special_identity': models.CharField(verbose_name="客户特殊身份", max_length=32, null=True,
                                                      blank=True),
        'is_word_of_mouth_publicity': models.CharField(verbose_name="是否做口碑宣传", max_length=8, null=True,
                                                       blank=True),
        'user_think_timely_response': models.CharField(verbose_name="用户认为是否及时响应", max_length=8, null=True,
                                                       blank=True),
        'user_think_solved': models.CharField(verbose_name="用户认为是否解决", max_length=8, null=True, blank=True),
        'user_satisfaction': models.CharField(verbose_name="用户是否满意", max_length=8, null=True, blank=True),
        'word_of_mouth_unmet_reason': models.TextField(verbose_name="口碑未达情况原因", null=True, blank=True),
        'whole_order_time_limit': models.IntegerField(verbose_name="整单时限", null=True, blank=True),

        # ===================== 子工单及APP处理字段 =====================
        'is_generate_sub_work_order': models.CharField(verbose_name="是否生成子工单", max_length=8, null=True,
                                                       blank=True),
        'is_app_process_link': models.CharField(verbose_name="是否有APP处理环节", max_length=8, null=True, blank=True),
        'app_process_link': models.CharField(verbose_name="APP处理环节", max_length=64, null=True, blank=True),
        'app_processor_name': models.CharField(verbose_name="APP处理人姓名", max_length=32, null=True, blank=True),
        'app_processor_account': models.CharField(verbose_name="APP处理人账号", max_length=32, null=True, blank=True),
        'app_process_time': models.DateTimeField(verbose_name="APP处理时间", null=True, blank=True),
        'app_processor_is_upload_img': models.CharField(verbose_name="APP处理人是否上传图片", max_length=8, null=True,
                                                        blank=True),
        'special_user_identifier': models.CharField(verbose_name="特殊用户标识", max_length=32, null=True, blank=True),
    }
