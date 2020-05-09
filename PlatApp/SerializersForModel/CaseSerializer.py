#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019-08-22
# @Author  : AngesZhu
# @File    : CaseSerializer.py
# @desc    : model序列化
from PlatApp.SerializerType.ManyKeyType import ManyKey
from PlatApp.models import CaseInfoForCaseCenter, CaseStepForCaseCenter, CaseSuiteForCaseCenter

from rest_framework import serializers


class CaseSuiteSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试套件序列化， 新增用
    """
    # case_id = serializers.CharField(allow_blank=True)

    class Meta:
        model = CaseSuiteForCaseCenter
        # fields = ('suite_name', 'case_id', 'description', 'created_by_id', 'updated_by_id')
        fields = ('suite_name', 'description', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        return CaseSuiteForCaseCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"],pro_id=self.context["pro_id"], case_type_id=self.context["case_type"], **validated_data)


class CaseSuiteListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试套件序列化，查询和列表
    """
    pro_name = serializers.CharField(source='pro.project_name')
    pro_id = serializers.ReadOnlyField()
    case_type_name = serializers.CharField(source='case_type.param_name')
    case_type_id = serializers.ReadOnlyField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = CaseSuiteForCaseCenter
        fields = ('id', 'suite_name', 'pro_name', 'pro_id', 'abandon_flag', 'case_type_name', 'case_type_id', 'case_id', 'description', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class CaseInfoSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试信息序列化，新增用
    """
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = CaseInfoForCaseCenter
        # fields = ('case_name', 'step_list', 'description', 'created_by_id', 'updated_by_id')
        fields = ('case_name', 'description', 'created_by_id', 'updated_by_id')

    def create(self, validated_data):
        if self.context.__contains__("case_suite_id"):
            return CaseInfoForCaseCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"],pro_id=self.context["pro_id"], case_type_id=self.context["case_type"], case_suite_id=self.context["case_suite_id"], **validated_data)
        else:
            return CaseInfoForCaseCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"],pro_id=self.context["pro_id"], case_type_id=self.context["case_type"], **validated_data)


class CaseInfoListSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试信息序列化，查询和列表
    """
    pro_name = serializers.CharField(source='pro.project_name')
    pro_id = serializers.ReadOnlyField()
    case_type_name = serializers.CharField(source='case_type.param_name')
    case_type_id = serializers.ReadOnlyField()
    step_list = ManyKey()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = CaseInfoForCaseCenter
        fields = ('id', 'case_name', 'pro_name', 'pro_id', 'case_type_name', 'case_type_id', 'abandon_flag','step_list', 'description', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def get_created_by(self, obj):
        return str(obj.created_by.last_name) + str(obj.created_by.first_name)

    def get_updated_by(self, obj):
        return str(obj.updated_by.last_name) + str(obj.updated_by.first_name)


class CaseStepSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 测试步骤序列化
    """
    save_list = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    execute_info = serializers.CharField(allow_blank=True)
    param_info = serializers.CharField(allow_blank=True)

    class Meta:
        model = CaseStepForCaseCenter
        # fields = "__all__"
        fields = ('step_type', 'step_id', 'case', 'execute_type', 'execute_info', 'for_id', 'check_type', 'save_list', 'execute_info', 'param_info', 'description')

    def create(self, validated_data):
        return CaseStepForCaseCenter.objects.create(updated_by_id=self.context["updated_by_id"], created_by_id=self.context["created_by_id"], **validated_data)
