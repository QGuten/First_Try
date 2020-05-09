# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :
from rest_framework import serializers

from django.forms import model_to_dict


class ManyKey(serializers.Field):
    """
    @Author: 朱孟彤
    @desc: 多对多外键数据处理
    """
    def to_representation(self, value):
        """
        多对多外键数据转换为列表输出
        :param value:
        :return:
        """
        a = value.all()
        step_list = []
        for i in a:
            step_list.append(model_to_dict(i))
        return step_list


class ManyKeyForTitle(serializers.Field):
    """
    @Author: 朱孟彤
    @desc: 多对多外键数据处理
    """
    def to_representation(self, value):
        """
        多对多外键数据转换为列表输出
        :param value:
        :return:
        """
        a = value.all()
        step_list = []
        for i in a:
            step_list.append(i.title)
        return step_list


class ManyKeyForName(serializers.Field):
    """
    @Author: 朱孟彤
    @desc: 多对多外键数据处理
    """
    def to_representation(self, value):
        """
        多对多外键数据转换为列表输出
        :param value:
        :return:
        """
        a = value.all()
        step_list = []
        for i in a:
            step_list.append(i.project_name)
        return step_list
