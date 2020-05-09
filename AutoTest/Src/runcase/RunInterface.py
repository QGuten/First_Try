#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :
import logging

logger = logging.getLogger('AutoTest')

from django.core.cache import cache

from AutoTest.Src.common.RunMethod import Http
from AutoTest.Src.common.AssertMethod import GetData
from AutoTest.Src.functions.PerformDistribution import ExeStep

from ast import literal_eval


class RunInterface:
    """
    用例分发执行
    """
    def __init__(self):
        # 储存执行结果
        self.res = {}
        # 统计数据初始化

        # 储存测试用例统计
        self.res['setup_count'] = {
            "all_num": 0,
            "pass_num": 0,
            "fail_num": 0,
        }

        # 储存测试用例统计
        self.res['case_count'] = {
            "all_num": 0,
            "pass_num": 0,
            "fail_num": 0,
        }
        # 储存测试用例步骤统计
        self.res["case_step_count"] = {
            "all_num": 0,
            "pass_num": 0,
            "fail_num": 0,
        }
        # 储存前提条件步骤统计
        self.res["setup_step_count"] = {
            "all_num": 0,
            "pass_num": 0,
            "fail_num": 0,
        }

    def choice(self, info: dict):
        """
        用例分发执行
        :param info: 传入参数为redis中储存的key组合成的字典
        :return: 返回执行结果
        """
        logger.info("---> 开始执行测试任务，储存key字典：{}".format(info))
        logger.info("---> 获取前提条件和用例数据")
        # 获取前提条件key数据
        setup_keys = info['job_setup']
        # 获取用例key数据
        case_keys = info['job_case']

        # setup_results = []

        logger.info("---> 初始化统计数据")

        # 根据传入的key字典，判断需要执行的数据数量
        self.res['setup_count']['all_num'] = len(setup_keys)
        self.res['case_count']['all_num'] = len(case_keys)
        if len(setup_keys) != 0:
            for i in setup_keys:
                self.res["setup_step_count"]["all_num"] += len(i["step_keys"])
        if len(case_keys) != 0:
            for j in case_keys:
                self.res["case_step_count"]["all_num"] += len(j["step_keys"])

        logger.info("---> 开始执行")

        # 获取任务执行时需要的参数：域名、header、验签参数
        job_info = cache.get(info["job_info"])

        cache_key = info["cache_key"]

        # 前提条件
        if len(setup_keys) != 0:
            # 前提条件数量为0时不调用
            logger.info("---> 任务中有前提条件")

            logger.info("---> 开始单独前提条件循环执行")

            for setup_key in setup_keys:
                # setup_keys前提条件key列表
                # setup_key是每一条前提条件key列表

                logger.info("---> 开始执行的前提条件, 用例key：{}".format(setup_key))

                key = setup_result = ''

                logger.info("初始化立即执行的前提条件的步骤执行数据统计")

                # 储存前提条件步骤统计
                setup_step_count = {
                    "all_num": 0,
                    "pass_num": 0,
                    "fail_num": 0,
                }

                logger.info("立即执行的前提条件的数据统计：{}".format(setup_step_count))

                for step in setup_key['step_keys']:
                    # 获取用例中的步骤列表

                    logger.info("---> 开始执行用例步骤")

                    step["result_key"] = step["info_key"].replace('step_info', 'result')
                    step["exe_info_key"] = step["info_key"].replace('step_info', 'exe_info')

                    # 获取步骤执行数据
                    setup_info = cache.get(step["info_key"])  # step["info_key"] 传入参数

                    logger.info("---> 用例步骤信息：{}".format(setup_info))

                    exe_step = ExeStep(job_info, cache_key)

                    exe_reslut = exe_step.runStep(setup_info, step["info_key"])

                    if exe_reslut['code'] == 20:
                        setup_step_count["pass_num"] += 1
                    else:
                        setup_step_count["fail_num"] += 1

                # 判断整体前提条件的执行结果，并统计
                if setup_step_count["fail_num"] == 0:
                    # 如果测试步骤失败统计为0，那么用例执行结果为通过
                    setup_result = "Success"
                    self.res["setup_count"]["pass_num"] += 1
                    logger.info("测试步骤失败统计为0，用例执行结果：{}".format(setup_result))
                else:
                    # 如果前提条件中，有步骤执行失败，那么整个前提条件执行结果视为未通过
                    setup_result = "Failed"
                    self.res["setup_count"]["fail_num"] += 1
                    logger.info("测试步骤失败统计不为0，用例执行结果：{}".format(setup_result))

                logger.info("---> 统计数据执行完毕")

                logger.info("---> 添加用例执行结果至redis缓存")

                setup_result_key = setup_key['case_info'].replace('case_info', 'result')

                cache.set(setup_result_key, setup_result, timeout=9999999999)

                setup_key['exe_result'] = setup_result_key

                logger.info("---> 添加用例执行结果至redis缓存成功")

            logger.info("---> 所有前提条件执行完毕")

        #  测试用例
        if len(case_keys) != 0 and self.res['setup_count']['fail_num'] == 0:
            # 测试用例数量为0时不调用
            logger.info("---> 任务中有测试用例")

            logger.info("---> 开始单独测试用例循环执行")

            for case_key in case_keys:
                # case_keys测试用例key列表
                # case_key是每一条测试用例key列表

                logger.info("---> 开始执行的测试用例, 用例key：{}".format(case_key))

                key = case_result = ''

                logger.info("初始化立即执行的测试用例的步骤执行数据统计")

                # 储存测试用例步骤统计
                case_step_count = {
                    "all_num": 0,
                    "pass_num": 0,
                    "fail_num": 0,
                }

                logger.info("立即执行的测试用例的数据统计：{}".format(case_step_count))

                for step in case_key['step_keys']:
                    # 获取用例中的步骤列表

                    logger.info("---> 开始执行用例步骤")

                    step["result_key"] = step["info_key"].replace('step_info', 'result')
                    step["exe_info_key"] = step["info_key"].replace('step_info', 'exe_info')

                    # 获取步骤执行数据
                    case_info = cache.get(step["info_key"])   # step["info_key"] 传入参数

                    logger.info("---> 用例步骤信息：{}".format(case_info))

                    exe_step = ExeStep(job_info, cache_key)

                    exe_reslut = exe_step.runStep(case_info, step["info_key"])

                    if exe_reslut['code'] == 20:
                        case_step_count["pass_num"] += 1
                    else:
                        case_step_count["fail_num"] += 1

                # 判断整体测试用例的执行结果，并统计
                if case_step_count["fail_num"] == 0:
                    # 如果测试步骤失败统计为0，那么用例执行结果为通过
                    case_result = "Success"
                    self.res["case_count"]["pass_num"] += 1
                    logger.info("测试步骤失败统计为0，用例执行结果：{}".format(case_result))
                else:
                    # 如果测试用例中，有步骤执行失败，那么整个测试用例执行结果视为未通过
                    case_result = "Failed"
                    self.res["case_count"]["fail_num"] += 1
                    logger.info("测试步骤失败统计不为0，用例执行结果：{}".format(case_result))

                logger.info("---> 统计数据执行完毕")

                logger.info("---> 添加用例执行结果至redis缓存")

                case_result_key = case_key['case_info'].replace('case_info', 'result')

                cache.set(case_result_key, case_result, timeout=9999999999)

                case_key['exe_result'] = case_result_key

                logger.info("---> 添加用例执行结果至redis缓存成功")

            logger.info("---> 所有测试用例执行完毕")
        else:
            logger.info("---> 测试用例数量为0或前置条件执行失败")

        logger.info("---> 更新job_keys")

        cache.set(info["job_keys"], info, timeout=9999999999)

        logger.info("---> 更新job_keys成功")

        return self.res
