# -*- coding: utf-8 -*-
# @Author  : AngesZhu
# @desc    : model序列化

from PlatApp.models import JobInfoForJobCenter, JobReportInfoForJobCenter, JobDataForJobCenter, \
    JobReportListForJobCenter, JobReportInfoForJobCenter, IterationForJobCenter, SubJobInfoForJobCenter, \
    SubJobDataForJobCenter, IterationRecordForJobCenter
from PlatApp.SerializerType.ReportCountType import ReportCount

from rest_framework import serializers


class JobInfoSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试任务序列化， 新增用
    """
    autograph_config = serializers.CharField(allow_blank=True)

    class Meta:
        model = JobInfoForJobCenter
        fields = ('job_name', 'job_state', 'domain_path', 'global_list', 'header_data', 'autograph_config', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return JobInfoForJobCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], pro_id=self.context["pro_id"], job_type_id=self.context["job_type"],
                                                  **validated_data)


class JobInfoListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试任务序列化， 查询和列表
    """
    pro_name = serializers.CharField(source='pro.project_name')
    pro_id = serializers.ReadOnlyField()
    job_type_name = serializers.CharField(source='job_type.param_name')
    job_type_id = serializers.ReadOnlyField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = JobInfoForJobCenter
        fields = ('id', 'job_name', 'job_state', 'abandon_flag', 'global_list', 'domain_path', 'header_data', 'autograph_config', 'pro_name', 'pro_id', 'job_type_name', 'job_type_id', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class SubJobInfoSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试子任务序列化， 新增用
    """
    autograph_config = serializers.CharField(allow_blank=True)

    class Meta:
        model = SubJobInfoForJobCenter
        fields = ('job_name', 'job_state', 'domain_path', 'global_list', 'header_data', 'autograph_config', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return SubJobInfoForJobCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], job_id=self.context["job_id"], pro_id=self.context["pro_id"], job_type_id=self.context["job_type"], **validated_data)


class SubJobInfoListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试子任务序列化， 查询和列表
    """
    pro_name = serializers.CharField(source='pro.project_name')
    pro_id = serializers.ReadOnlyField()
    job_type_name = serializers.CharField(source='job_type.param_name')
    job_type_id = serializers.ReadOnlyField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = SubJobInfoForJobCenter
        fields = ('id', 'job_name', 'domain_path', 'abandon_flag', 'global_list', 'header_data', 'autograph_config', 'job_state', 'pro_name', 'pro_id', 'job_type_name', 'job_type_id', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class SubJobDataSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试子任务数据关系表序列化， 新增用
    """
    save_list = serializers.CharField(allow_blank=True)
    domain_path = serializers.CharField(allow_blank=True)

    class Meta:
        model = SubJobDataForJobCenter
        fields = ('if_setup', 'exe_step', 'domain_path', 'save_list', 'exe_data', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return SubJobDataForJobCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], job_id=self.context["job_id"], case_id=self.context["case_id"],
                                                  **validated_data)


class JobDataSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试任务数据关系表序列化， 新增用
    """
    save_list = serializers.CharField(allow_blank=True)
    domain_path = serializers.CharField(allow_blank=True)

    class Meta:
        model = JobDataForJobCenter
        fields = ('if_setup', 'exe_step', 'domain_path', 'save_list', 'exe_data', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return JobDataForJobCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], job_id=self.context["job_id"], case_id=self.context["case_id"],
                                                  **validated_data)


class JobReportListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试报告列表序列化， 新增用
    """
    case_count = serializers.CharField(allow_blank=True)
    setup_count = serializers.CharField(allow_blank=True)
    setup_exe_count = serializers.CharField(allow_blank=True)
    case_exe_count = serializers.CharField(allow_blank=True)

    class Meta:
        model = JobReportListForJobCenter
        fields = ('report_name', 'start_at', 'case_count', 'setup_count', 'setup_exe_count', 'case_exe_count', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return JobReportListForJobCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], job_id=self.context["job_id"], **validated_data)


class JobReportListDeSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试报告列表序列化， 查询和列表
    """
    job_name = serializers.CharField(source='job.job_name')
    job_id = serializers.ReadOnlyField()
    case_count = ReportCount()
    case_exe_count = ReportCount()
    setup_count = ReportCount()
    setup_exe_count = ReportCount()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = JobReportListForJobCenter
        fields = ('id', 'start_at', 'report_name', 'case_count', 'setup_exe_count', 'case_exe_count', 'setup_count', 'job_name', 'job_id', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class JobReportInfoSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试报告详情序列化， 新增用
    """
    case_id = serializers.CharField(allow_null=True)
    step_id = serializers.CharField(allow_null=True)
    description = serializers.CharField(allow_null=True)

    class Meta:
        model = JobReportInfoForJobCenter
        fields = ('case_id', 'step_id', 'exe_info', 'result_info', 'created_by_id', 'updated_by_id', 'description')

    def create(self, validated_data):
        return JobReportInfoForJobCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], report_id=self.context["report_id"], **validated_data)


class JobReportDetailSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试报告详情序列化，获取用
    """
    case_name = serializers.CharField(source='case.case_name')
    case_id = serializers.ReadOnlyField()
    step_id = serializers.ReadOnlyField()

    class Meta:
        model = JobReportInfoForJobCenter
        fields = ('id', 'case_id', 'case_name', 'step_id', 'exe_info', 'result_info', 'created_by', 'updated_by', 'created_at',
                  'start_at', 'created_by', 'description')


class IterationSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 迭代表序列化， 新增用
    """

    class Meta:
        model = IterationForJobCenter
        fields = ('name', 'state', 'description', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return IterationForJobCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], pro_id=self.context["pro_id"], version_id=self.context["version_id"], **validated_data)


class IterationListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 迭代表序列化， 查询和列表
    """
    pro_name = serializers.CharField(source='pro.project_name')
    pro_id = serializers.ReadOnlyField()
    version_name = serializers.CharField(source='version.type')
    version_id = serializers.ReadOnlyField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = IterationForJobCenter
        fields = ('id', 'name', 'state', 'description', 'abandon_flag', 'pro_name', 'pro_id', 'version_id', 'version_name', 'created_by', 'updated_by', 'created_at', 'updated_at')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class IterationRecordSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 迭代执行记录表序列化， 新增用
    """
    exe_overview = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = IterationRecordForJobCenter
        # fields = ('exe_overview', 'description', 'created_by_id', 'updated_by_id')
        fields = ('exe_overview', 'description')

    def create(self, validated_data):
        return IterationRecordForJobCenter.objects.create(it_id=self.context["it_id"], updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], **validated_data)


class IterationListRecordSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 迭代执行记录表序列化， 查询和列表
    """
    it_name = serializers.CharField(source='it.name')
    it_id = serializers.ReadOnlyField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = IterationRecordForJobCenter
        fields = ('id', 'exe_overview', 'description', 'abandon_flag', 'it_id', 'it_name', 'created_by', 'updated_by', 'created_at', 'updated_at')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)