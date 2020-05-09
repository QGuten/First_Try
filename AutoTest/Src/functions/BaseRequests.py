# -*- coding: utf-8 -*-
# @Time    : 20181126
# @Author  : AngesZhu
# @File    : BaseRequests.py
# @desc:请求方法封装
from AutoTest.Src.common.DubboRequests import Dubbo
from AutoTest.Src.common.RestfulRequests import *


def send_requests(send_info):
    """
    @Author: 朱孟彤
    @desc: 发送restful接口方法
    :param 请求数据:
    :return:
    """
    if send_info['type'] == 'dubbo':
        if isinstance(send_info, dict):
            info = send_info
            conn = Dubbo(info['host'], info['post'])
            result = conn.invoke_json(send_info)
            conn.close()
            return result
        else:
            return {'errorCode': 40010, 'message': '请求参数错误'}

    elif send_info['type'] == 'restFul':
        if isinstance(send_info, dict):
            result = send_restFul(send_info)
            return result
        else:
            return {'errorCode': 40010, 'message': '请求参数错误'}

    elif send_info['type'] == 'activeMQ':
        pass

    elif send_info['type'] == 'rabbitMQ':
        pass

    else:
        return {'errorCode': 40010, 'message': '请求参数错误'}
