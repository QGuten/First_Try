# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @desc    :
from PlatApp.models import ConfigForResources, RequestsForResources

from rest_framework import serializers


class ConfigForResourcesSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 资源库配置序列化，新增数据用
    """
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = ConfigForResources
        fields = ('id', 'key', 'value', 'name', 'description', 'abandon_flag')

    def create(self, validated_data):
        return ConfigForResources.objects.create(pro_id=self.context["pro_id"], updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], **validated_data)


class GetConfigForResourcesSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 资源库配置序列化，获取数据用
    """
    project_name = serializers.CharField(source='pro.project_name')
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ConfigForResources
        fields = ('id', 'key', 'value', 'name', 'description', 'project_name', 'abandon_flag', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class RequestsForResourcesSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 资源库接口文档配置，新增用
    """
    developer = serializers.CharField(allow_blank=True)
    re_response = serializers.CharField(allow_blank=True)
    re_name = serializers.CharField(allow_blank=True)
    edition = serializers.CharField(allow_blank=True)
    re_params = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = RequestsForResources
        fields = ('id', 'serial_number', 're_name', 're_path', 're_method', 'developer', 'project_id',
                  're_params', 're_response', 'description', 'abandon_flag', 'edition')

    def create(self, validated_data):
        return RequestsForResources.objects.create(project_id=self.context["project_id"], updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], **validated_data)


class RequestsListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 资源库接口文档列表查询
    """
    project_name = serializers.CharField(source='project.project_name')
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = RequestsForResources
        fields = ('id', 're_name', 're_method', 're_path', 'developer', 'project_name', 'edition', 'if_have_case', 'abandon_flag', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)
