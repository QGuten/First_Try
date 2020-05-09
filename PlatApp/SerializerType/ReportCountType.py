# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :
from ast import literal_eval

from rest_framework import serializers

from django.forms import model_to_dict


class ReportCount(serializers.Field):
    """
    @Author: 朱孟彤
    @desc: 测试报告信息数据序列化中处理展示信息
    """
    def to_representation(self, value):
        """
        测试报告信息数据序列化中处理展示信息
        {'case_count': 1, 'case_succeed': 1, 'case_fail': 0}
        :param value:
        :return:
        """
        if value:

            data = literal_eval(value)

            return_data = ''

            if isinstance(data, dict):
                for key in data.keys():
                    if "count" in key:
                        return_data += '共计数量：' + str(data[key]) + '\n'
                    elif "succeed" in key:
                        return_data += '执行成功数量：' + str(data[key]) + '\n'
                    elif "fail" in key:
                        return_data += '执行失败数量：' + str(data[key]) + '\n'

            return return_data

        else:

            return ''
