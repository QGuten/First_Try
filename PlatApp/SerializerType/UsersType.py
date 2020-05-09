# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @desc    :
import time
import datetime

from rest_framework import serializers


class TimestampField(serializers.Field):
    """
    @Author: 朱孟彤
    @desc: 时间序列化格式自定义
    """
    def to_representation(self, value):
        """
        数据库时间类型转换为时间戳类型输出
        :param value:
        :return:
        """
        return int(time.mktime(value.timetuple()))*1000

    def to_internal_value(self, data):
        """
        时间戳类型反序列化python时间类型
        :param data:
        :return:
        """
        return datetime.datetime.fromtimestamp(int(data)*1000)


class NameField(serializers.Field):
    """
    @Author: 朱孟彤
    @desc: 完整的用户名拼接
    """
    def to_representation(self, *value):
        """
        把姓 和 名拼接成一个完整的名字
        :param value:
        :return:
        """
        name = ''.join(value)
        return name


if __name__ == '__main__':
    a = '1563808843'
    print(TimestampField().to_internal_value(a))
