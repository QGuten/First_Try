#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Kris
# @File    : 
# @desc    :
import logging

from django.http import JsonResponse

from rest_framework import status

logger = logging.getLogger('AutoApp.app')


class ReturnJson:
    """
    @Author: 朱孟彤
    @desc: 接口返回值封装
    """

    @staticmethod
    def success(data):
        return_info = {'data': data, 'code': 200}
        logger.info("接口请求成功，返回值为：" + str(return_info))
        return JsonResponse(return_info, status=status.HTTP_200_OK, safe=False)

    @staticmethod
    def faile(data):
        logger.error("接口请求失败，返回值为：" + str(data))
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST, safe=False)
