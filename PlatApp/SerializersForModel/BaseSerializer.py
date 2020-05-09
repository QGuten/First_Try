# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :
from PlatApp.models import ProjectForBase, BaseSysParam, JobForBase, JobRecordForBase, VersionForProject
from PlatApp.SerializerType.UsersType import TimestampField

from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 系统项目配置序列化，新增
    """
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = ProjectForBase
        fields = ('id', 'parent', 'project_name', 'project_type', 'project_code', 'description', 'abandon_flag', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        if self.context.__contains__("parent_id"):
            return ProjectForBase.objects.create(parent_id=self.context['parent_id'], updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], **validated_data)
        else:
            return ProjectForBase.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], **validated_data)


class ProjectListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 系统项目配置序列化，列表和查询
    """
    parent_name = serializers.CharField(source='parent.project_name', allow_null=True)
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ProjectForBase
        fields = ('id', 'parent_name', 'project_name', 'project_type', 'project_code', 'description', 'abandon_flag', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class VersionForProjectSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 项目版本号配置序列化，新增
    """
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = VersionForProject
        fields = ('pro_id', 'type', 'description', 'abandon_flag', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return VersionForProject.objects.create(pro_id=self.context["pro_id"], updated_by_id=self.context["updated_by_id"],
                                                    created_by_id=self.context["created_by_id"], **validated_data)


class VersionForProjectListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 项目版本号配置序列化，列表和查询
    """
    pro = serializers.CharField(source='pro.project_name', allow_null=True)
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = VersionForProject
        fields = ('id', 'pro', 'type', 'description', 'abandon_flag', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class BaseSysParamSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 系统参数配置序列化，新增
    """
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = BaseSysParam
        fields = ('id', 'param_key', 'param_value', 'param_name', 'description', 'abandon_flag', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return BaseSysParam.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], **validated_data)


class BaseSysParamListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 系统参数配置序列化，列表和查询
    """
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = BaseSysParam
        fields = ('id', 'param_key', 'param_value', 'param_name', 'description', 'abandon_flag', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class JobForBaseSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 系统任务配置序列化，新增
    """
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = JobForBase
        fields = ('id', 'name', 'state', 'description', 'abandon_flag')


class JobRecordForBaseSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 系统任务执行记录序列化，新增
    """
    description = serializers.CharField(allow_blank=True)
    date = serializers.CharField(allow_blank=True)
    explain = serializers.CharField(allow_blank=True)

    class Meta:
        model = JobRecordForBase
        fields = ('id', 'job_id', 'params', 'date', 'explain', 'description', 'abandon_flag')

    def create(self, validated_data):
        return JobRecordForBase.objects.create(job_id=self.context["job_id"], **validated_data)
