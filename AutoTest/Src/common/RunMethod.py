#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import logging
import time
import os

from requests.packages import urllib3

from django.core.cache import cache
# from AutoTest.functions.SignForMagicBean import Sign
from AutoTest.Common.PathHandle import PathGet
from AutoTest.Common.TestConfig import IniOperation

logger = logging.getLogger('AutoTest')

# 关闭警告信息
urllib3.disable_warnings()


class Http:
    """
    Http方法请求
    """

    def __handle_data(self, cache_info, data_info):
        """
        数据处理拼接
        :param cache_info: 字段缓存池
        :param header_info: 请求头信息
        :return:
        """
        data = {}

        for key, value in data_info.items():

            if value[0:2] == "${" and value[-1] == "}":

                cache_name = value[2:-1]
                if cache_info and cache_info.__contains__(cache_name):
                    data[key] = cache_info[cache_name]
                else:
                    pass
                    # headers[key] = ""
            elif key == '' or value == '':
                pass
            else:
                data[key] = value

        return data

    def __handle_path(self, domain_path, re_path):
        """
        请求地址拼接处理
        :param domain_path: 请求域名
        :param re_path: 请求地址
        :return:
        """
        if domain_path[-1] == "/" and re_path[0] == "/":
            url = domain_path[:-1] + re_path
        elif domain_path[-1] == "/" or re_path[0] == "/":
            url = domain_path + re_path
        else:
            url = domain_path + '/' + re_path
        return url

    def __get_signature(self, headers, url, exe_info):

        pathObj = PathGet()
        path = pathObj.getfile(pathObj.getfile(pathObj.getpath()))
        py_path = pathObj.addpath(path, 'functions')
        ini_path = pathObj.addpath(path, 'Config', 'SignConfig.ini')

        ini_obj = IniOperation()
        ini_obj.OpenIni(ini_path)
        ini_obj.NewOption('sign_info', 'appkey', headers['bt-auth-appkey'])
        ini_obj.NewOption('sign_info', 'secretkey', headers['bt-auth-nonce'])
        ini_obj.NewOption('sign_info', 'url', url)
        ini_obj.NewOption('sign_info', 'param', str(exe_info))
        ini_obj.NewOption('sign_info', 'timestamp', headers['bt-auth-timestamp'])
        ini_obj.WriteIni(ini_path)

        # cmd_1 = "cd {}".format(py_path)
        cmd = "python3 {}/SignForMagicBean.py".format(py_path)
        print(cmd)

        try:

            os.system(cmd)

            re_data = ini_obj.GetOption('result', 'info', 'str')

            return {'code': 20, 'data': re_data}
        except Exception as e:
                return {'code': 110, 'msg': e}
        # data = {}
        # data['timestamp'] = headers['bt-auth-timestamp']
        # data['appkey'] = headers['bt-auth-appkey']
        # # data['secretkey'] = headers['secretkey']
        # data['secretkey'] = headers['bt-auth-nonce']
        # data['url'] = url
        # data['param'] = exe_info
        # s_obj = Sign()
        # re_data = s_obj.get_signature('sign.jar', 'com.test.TestGenerateSign', data)

    def __init__(self, job_info: dict, cache_key):
        # 子任务信息中提取任务级参数
        self.domain_path = job_info['domain_path']
        self.autograph_config = job_info['autograph_config']
        self.header_data = job_info['header_data']
        # 缓存key
        self.cache_key = cache_key

    def getRun(self, info: dict, key_header: str):
        """
        接口执行分发入口
        :param info: 接口执行数据
        :return: 接口执行结果
        """
        self.key_header = key_header

        logger.info("---> 开始执行HTTP方法请求")
        re_result = ''
        method = info['re_method']
        if method == 'GET':
            # 调用get方法
            logger.info("---> 请求为GET请求")
            re_result = self.runGet(info)

        if method == 'POST':
            # 调用post
            logger.info("---> 请求为POST请求")
            re_result = self.runPost(info)

        # if method == 'PUT':
        #     # 调用put
        #     logger.info("---> 请求为PUT请求")
        #     re_result = self.runPut(info)

        return re_result

    def runGet(self, case):

        logger.info("---> 开始执行GET请求")

        res = {}  # 接受返回数据

        logger.info("---> 获取、拼接请求数据")

        cache_info = cache.get(self.cache_key)

        header_info = eval(self.header_data)

        headers = [self.__handle_data(cache_info, i) for i in header_info]

        header = {}

        for h in headers:
            for k, b in h.items():
                header[k] = b

        if case['domain_path']:
            url = self.__handle_path(case['domain_path'], case['re_path'])
        else:
            url = self.__handle_path(self.domain_path, case['re_path'])

        # data = case['exe_params']
        data = self.__handle_data(cache_info, case['exe_params'])

        if self.autograph_config == "Sign":
            header['bt-auth-timestamp'] = str(int(time.time() * 1000))
            res = self.__get_signature(header, case['re_path'], data)
            if res['code'] == 20:
                header['bt-auth-sign'] = res['data']
            else:
                return '签名获取错误'

        cache.set(self.key_header + "exe_info", {
            'url': url,
            'data': data,
            'headers': header
        }, timeout=9999999999)

        logger.info("请求url：{}".format(url))
        logger.info("请求data：{}".format(data))
        logger.info("请求headers：{}".format(header))

        logger.info("---> 开始请求接口")
        try:
            a = requests.get(url, params=data, headers=header, verify=False)
            # a = requests.get(url, json=data, headers=header, verify=False)
        except Exception as ex:
            logger.info("---> 接口请求失败")
            return str(ex)

        logger.info("---> 开始拼接返回数据")

        res["http_status_code"] = str(a.status_code)  # 状态码转成str
        res["text"] = a.content.decode("utf-8")
        # res["headers"] = a.headers
        res["times"] = str(a.elapsed.total_seconds())  # 接口请求时间转str
        if res["http_status_code"] != '200':
            res["error"] = res["text"]
        else:
            res["error"] = ""
            logger.info("---> 检测储存参数")

        logger.info("---> 执行GET请求完毕")
        return res

    def runPost(self, case):

        logger.info("---> 开始执行POST请求")

        res = {}  # 接受返回数据

        logger.info("---> 获取、拼接请求数据")

        cache_info = cache.get(self.cache_key)

        header_info = eval(self.header_data)

        # headers = self.__handle_data(cache_info, header_info)
        headers = [self.__handle_data(cache_info, i) for i in header_info]

        header = {}

        # header['user-agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'

        for h in headers:
            for k, b in h.items():
                header[k] = b

        if case['domain_path']:
            url = self.__handle_path(case['domain_path'], case['re_path'])
        else:
            url = self.__handle_path(self.domain_path, case['re_path'])

        # data = [self.__handle_data(cache_info, i) for i in case['exe_params']]
        data = self.__handle_data(cache_info, case['exe_params'])

        if self.autograph_config == "Sign":
            header['bt-auth-timestamp'] = str(int(time.time() * 1000))
            res = self.__get_signature(header, case['re_path'], data)
            if res['code'] == 20:
                header['bt-auth-sign'] = res['data']
            else:
                return '签名获取错误'

        cache.set(self.key_header + "exe_info", {
            'url': url,
            'data': data,
            'headers': header
        }, timeout=9999999999)

        logger.info("请求url：{}".format(url))
        logger.info("请求data：{}".format(data))
        logger.info("请求headers：{}".format(header))

        try:
            logger.info("---> 开始请求接口")
            # a = requests.post(url, data=data, headers=header, verify=False)
            a = requests.post(url, json=data, headers=header, verify=False)
        except Exception as ex:
            logger.info("---> 接口请求失败")
            return str(ex)
        logger.info("---> 接口请求成功，返回值为：{}".format(a))
        logger.info("---> 开始拼接返回数据")
        res["http_status_code"] = str(a.status_code)  # 状态码转成str
        # res["headers"] = a.headers
        logger.info("---> 接口请求成功，headers为：{}".format(a.headers))
        # res["text"] = a.content.decode("utf-8")
        res["text"] = a.json()
        res["times"] = str(a.elapsed.total_seconds())  # 接口请求时间转str
        if res["http_status_code"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
            logger.info("---> 检测储存参数")

        logger.info("---> 执行POST请求完毕")
        return res
