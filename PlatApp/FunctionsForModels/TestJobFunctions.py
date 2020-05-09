# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :

import time
import logging

from django.forms import model_to_dict
from django.core.cache import cache

from PlatApp.models import SubJobInfoForJobCenter, SubJobDataForJobCenter, CaseInfoForCaseCenter, RequestsForResources, JobReportListForJobCenter

from PlatApp.SerializersForModel.JobInfoSerializer import JobInfoSerializer, JobDataSerializer, JobReportListSerializer, \
    JobReportInfoSerializer

from AutoTest.Src.runcase.RunInterface import RunInterface

logger = logging.getLogger('AutoApp.app')


class ExeSubJob:
    """
    @Author: 朱孟彤
    @desc: 新增测试任务信息封装
    """

    def exeSubJob(self, job_id: int, user_id: int):
        """
        子任务执行
        :param job_id: 要执行的子任务ID
        :param user_id: 执行操作用户ID
        :return:
        """
        try:

            start_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

            # 获取任务基础信息
            logger.info("---> 开始获取任务基础信息")
            job_info = SubJobInfoForJobCenter.objects.get(id=int(job_id))

            # 创建任务执行报告
            logger.info("---> 拼接处理测试报告写入数据")

            report_info = {
                "case_count": '',
                "case_exe_count": '',
                "setup_count": '',
                "setup_exe_count": '',
                "report_name": str(job_info.job_name + '_' + start_at),
                "start_at": start_at
            }
            report_context = {
                "created_by_id": user_id,
                "updated_by_id": user_id,
                "job_id": job_id
            }

            logger.info("---> 拼接数据完毕，开始创建测试报告数据")

            report_result = self.__createJobReport({
                "data": report_info,
                "context": report_context,
            })
            if report_result['state'] == 110:
                return {'state': 110, 'errmsg': '测试报告创建异常！', 'data': report_result['data']}

            logger.info("---> 添加测试报告信息至报告信息表成功")

            logger.info("---> 开始添加全局变量至缓存池")

            key_obj = self.__getDataSaveToRedis(job_id=job_id, job_info=job_info)

            if key_obj['state'] == 110:
                return {'state': 110, 'errmsg': '添加全局变量至缓存池异常', 'data': key_obj['data']}

            keys = key_obj['data']

            logger.info("---> 添加全局变量至缓存池完毕")

            logger.info("---> 任务开始执行")

            try:

                run_connet = RunInterface()

                result = run_connet.choice(keys)

                logger.info(str(result))

                logger.info("---> 任务执行结束")

            except Exception as ex:
                logger.error(ex)
                return {'state': 110, 'errmsg': '任务执行异常', 'data': ex}

            logger.info("---> 开始添加测试报告相关信息")

            save_result = self.__writeReport(result, user_id, report_result['data'], keys)

            if save_result['state'] == 110:
                return {'state': 110, 'errmsg': '添加测试报告异常', 'data': save_result['data']}

            logger.info("---> 任务执行成功，请在报告管理中，查看任务状态。")

            logger.info("---> 任务执行结束，清除任务执行缓存。")

            clear_result = self.__clearData(keys)

            if clear_result['state'] == 110:
                return {'state': 110, 'errmsg': '清除缓存异常', 'data': clear_result['data']}

            return {'state': 200, 'data': int(report_result['data'])}

        except Exception as ex:

            return {'state': 110, 'data': ex}

    def __getDataSaveToRedis(self, job_id, job_info):
        """
        根据子任务ID获取数据并储存至缓存池
        :return:
        """
        # redis 存储key集合
        keys = {}

        try:

            job_key = "case_job:" + str(job_id) + "_" + str(int(time.time())) + ":"
            info_key = job_key + "job_info"
            keys["job_info"] = info_key  # 任务基础信息key
            cache.set(info_key, model_to_dict(job_info), timeout=9999999999)

            keys["cache_key"] = job_key + "params_cache"

            if job_info.global_list:

                global_data_l = eval(job_info.global_list)

                global_data = {}

                for g_data in global_data_l:
                    global_data.update(g_data)

                cache.set(job_key + "params_cache", global_data, timeout=9999999999)

            logger.info("---> 开始添加全局变量至缓存池完毕")

            # 获取任务数据信息
            logger.info("---> 开始获取任务数据信息")
            job_data_list = SubJobDataForJobCenter.objects.filter(job_id=int(job_id))
            logger.info("---> 获取任务数据信息成功")

            setup_list = []
            case_list = []

            # 根据是否是前提条件获取数据
            setup_dict = []
            case_dict = []
            logger.info("---> 开始根据任务数据信息，对任务数据信息进行处理，并添加数据至redis缓存")

            for job_data in job_data_list:

                # # 请求域名
                # domain_path = job_data.domain_path
                # # 请求头
                # header_data = job_data.header_data
                # 请求数据
                exe_data = eval(job_data.exe_data)
                # 储存参数
                save_list = job_data.save_list
                # 步骤请求域名
                domain_path = job_data.domain_path

                if job_data.if_setup:
                    # 判断数据是否是前提条件

                    setup_keys = []

                    # key_header = job_key + "job_setup:" + str(job_data.exe_step)
                    key_header = job_key + "job_setup:" + str(job_data.case_id)

                    # 根据case_id获取用例信息以及操作步骤列表
                    case_info = CaseInfoForCaseCenter.objects.get(id=int(job_data.case_id))

                    a = case_info.step_list.all()  # 操作步骤列表
                    step_list = [model_to_dict(i) for i in a]

                    case_info = model_to_dict(case_info)
                    case_info['step_list'] = step_list

                    cache.set(key_header + ":case_info", case_info, timeout=9999999999)

                    # 获取接口id，并获取接口数据
                    for data in exe_data:
                        # for step in step_list:
                        info = {}
                        # exe_data 查找数据中，步骤id相同的数据一起存储
                        # for data in exe_data:
                        if len(step_list) == 1:
                            info.update(step_list[0])
                            if step_list[0]["execute_type"] == "HTTP":
                                info.update(
                                    model_to_dict(RequestsForResources.objects.get(id=int(step_list[0]["for_id"]))))
                            # info['save_list'] = save_list
                            info['domain_path'] = domain_path
                            info["step_id"] = data['step_id']
                            # info["domain_path"] = domain_path
                            # info["header_data"] = header_data
                            # logger.info(data["data"])
                            # logger.info(type(data["data"]))
                            info.update(eval(data["data"]))
                            if not info.__contains__('save_list'):
                                info['save_list'] = save_list
                        else:
                            # 多步骤，数据匹配，预留位置
                            pass

                        setup_key = key_header + ":" + str(info["step_id"]) + ":step_info"
                        setup_keys.append({"info_key": setup_key})
                        # case_keys.append(case_keys)
                        # logger.info(str(info))
                        cache.set(setup_key, info, timeout=9999999999)

                    setup_dict.append({"case_info": key_header + ":case_info", "step_keys": setup_keys})

                else:
                    # 若不是前提条件，那么数据为测试用例
                    case_keys = []

                    # key_header = job_key + "job_case:" + str(job_data.exe_step)
                    key_header = job_key + "job_case:" + str(job_data.case_id)

                    # 根据case_id获取用例信息以及操作步骤列表
                    case_info = CaseInfoForCaseCenter.objects.get(id=job_data.case_id)

                    a = case_info.step_list.all()  # 操作步骤列表
                    step_list = [model_to_dict(i) for i in a]

                    case_info = model_to_dict(case_info)
                    case_info['step_list'] = step_list

                    cache.set(key_header + ":case_info", case_info, timeout=9999999999)

                    # 获取接口id，并获取接口数据
                    for data in exe_data:
                        # for step in step_list:
                        info = {}
                        # exe_data 查找数据中，步骤id相同的数据一起存储
                        # for data in exe_data:
                        if len(step_list) == 1:
                            info.update(step_list[0])
                            if step_list[0]["execute_type"] == "HTTP":
                                info.update(
                                    model_to_dict(RequestsForResources.objects.get(id=int(step_list[0]["for_id"]))))
                            # info['save_list'] = save_list
                            info['domain_path'] = domain_path
                            info["step_id"] = data['step_id']
                            # info["domain_path"] = domain_path
                            # info["header_data"] = header_data
                            # logger.info(data["data"])
                            # logger.info(type(data["data"]))
                            info.update(eval(data["data"]))
                            if not info['save_list']:
                                info['save_list'] = save_list
                        else:
                            # 多步骤，数据匹配，预留位置
                            pass

                        case_key = key_header + ":" + str(info["step_id"]) + ":step_info"
                        case_keys.append({"info_key": case_key})
                        # case_keys.append(case_keys)
                        # logger.info(str(info))
                        cache.set(case_key, info, timeout=9999999999)

                    case_dict.append({"case_info": key_header + ":case_info", "step_keys": case_keys})

            if len(setup_dict) != 0:
                setup_list.append(setup_dict)
            if len(case_dict) != 0:
                case_list.append(case_dict)

            # keys["job_setup"] = setup_list
            keys["job_setup"] = setup_dict
            # keys["job_case"] = case_list
            keys["job_case"] = case_dict
            keys["job_keys"] = job_key + "key_list"

            cache.set(job_key + "key_list", keys, timeout=9999999999)

            return {'state': 200, 'data': keys}
        except Exception as ex:
            return {'state': 110, 'data': ex}

    def __writeReport(self, result, user_id, report_id, keys):
        """
        执行完毕后的测试报告写入
        :param result:
        :param user_id:
        :param report_id:
        :return:
        """
        try:

            logger.info("---> 更新测试报告，写入数据")

            report_obj = JobReportListForJobCenter.objects.get(id=int(report_id))

            report_obj.case_count = str(result['case_count'])
            report_obj.case_exe_count = str(result['case_step_count'])
            report_obj.setup_count = str(result['setup_count'])
            report_obj.setup_exe_count = str(result['setup_step_count'])
            report_obj.status = 20

            report_obj.save()

            logger.info("---> 更新执行结果统计至测试报告信息成功")

            # 循环添加测试报告数据信息
            logger.info("---> 添加测试报告数据信息至报告详情表")

            for setup in keys['job_setup']:
                # 添加前置条件结果信息
                case_info_cache = cache.get(setup['case_info'])
                if not setup.__contains__('exe_result'):
                    break
                result_data_info = {
                    "case_id": int(case_info_cache["id"]),
                    "step_id": None,
                    "exe_info": str(case_info_cache),
                    "result_info": str(cache.get(setup['exe_result'])),
                    "description": "前置条件结果信息",
                }

                result_data_context = {
                    "created_by_id": user_id,
                    "updated_by_id": user_id,
                    "report_id": report_id
                }

                case_data = self.__createJobDataReport(result_data_info, result_data_context)
                if case_data['state'] == 110:
                    return {'state': 110, 'errmsg': '测试报告创建异常！', 'data': case_data['data']}

                for step in setup["step_keys"]:
                    step_info = cache.get(step['info_key'])
                    step_data_info = {
                        "case_id": int(case_info_cache["id"]),
                        "step_id": int(step_info["step_id"]),
                        "exe_info": str(cache.get(step['exe_info_key'])),
                        "result_info": str(cache.get(step['result_key'])),
                        "description": str(case_info_cache),
                    }
                    step_data_context = {
                        "created_by_id": user_id,
                        "updated_by_id": user_id,
                        "report_id": report_id
                    }
                    step_data = self.__createJobDataReport(step_data_info, step_data_context)
                    if step_data['state'] == 110:
                        return {'state': 110, 'errmsg': '测试报告创建异常！', 'data': step_data['data']}

            for case in keys['job_case']:
                # 先添加执行用例结果信息
                case_info_cache = cache.get(case['case_info'])
                if not case.__contains__('exe_result'):
                    break
                case_result_cache = cache.get(case['exe_result'])
                logger.info('测试用例执行结果：{}'.format(case_result_cache))
                result_data_info = {
                    "case_id": int(case_info_cache["id"]),
                    "step_id": None,
                    "exe_info": str(case_info_cache),
                    "result_info": case_result_cache,
                    "description": "执行用例结果信息",
                }
                logger.info("测试用例结果信息：{}".format(result_data_info))
                result_data_context = {
                    "created_by_id": user_id,
                    "updated_by_id": user_id,
                    "report_id": report_id
                }

                case_data = self.__createJobDataReport(result_data_info, result_data_context)
                if case_data['state'] == 110:
                    return {'state': 110, 'errmsg': '测试报告创建异常！', 'data': case_data['data']}

                for step in case["step_keys"]:
                    step_info = cache.get(step['info_key'])
                    step_data_info = {
                        "case_id": int(case_info_cache["id"]),
                        "step_id": int(step_info["step_id"]),
                        "exe_info": str(cache.get(step['exe_info_key'])),
                        "result_info": str(cache.get(step['result_key'])),
                        "description": str(case_info_cache),
                    }
                    step_data_context = {
                        "report_id": report_id,
                        "created_by_id": user_id,
                        "updated_by_id": user_id,
                    }

                    step_data = self.__createJobDataReport(step_data_info, step_data_context)
                    if step_data['state'] == 110:
                        return {'state': 110, 'errmsg': '测试报告创建异常！', 'data': step_data['data']}

            logger.info("---> 添加测试报告数据信息至报告详情表成功")

            return {'state': 200, 'data': ''}

        except Exception as ex:
            logger.error(ex)
            # transaction.rollback(sid)
            return {'state': 110, 'data': ex}

    def __clearData(self, keys):
        """
        根据Keys清空缓存池
        :param keys:
        :return:
        """
        try:
            if isinstance(keys, dict):
                for value in keys.values():
                    if isinstance(value, list):
                        for step_value in value:
                            if isinstance(step_value, dict):
                                for key_3 in step_value.values():
                                    if isinstance(key_3, str):
                                        cache.delete(key_3)
                                    if isinstance(key_3, list):
                                        for key_4 in key_3:
                                            if isinstance(key_4, dict):
                                                [cache.delete(key_5) for key_5 in key_4.values()]
                    if isinstance(value, str):
                        cache.delete(value)
            return {'state': 200, 'data': '数据清除成功！'}
        except Exception as ex:
            return {'state': 110, 'data': ex}

    def __createJobReport(self, data: dict):
        """
        根据数据创建测试报告
        :param data:
        :return:
        """
        try:
            new_report = JobReportListSerializer(data=data['data'], context=data['context'])
            new_report.is_valid(raise_exception=True)
            report_info = new_report.save()
            return {'state': 200, 'data': report_info.id}
        except Exception as ex:
            return {'state': 110, 'data': ex}

    def __createJobDataReport(self, data: dict, context: dict):
        """
        根据数据创建测试报告详情
        :param data:
        :return:
        """
        try:
            new_report = JobReportInfoSerializer(data=data, context=context)
            new_report.is_valid(raise_exception=True)
            report_info = new_report.save()
            return {'state': 200, 'data': report_info.id}
        except Exception as ex:
            return {'state': 110, 'data': ex}


class CreateJobData:
    """
    @Author: 朱孟彤
    @desc: 新增测试任务信息封装
    """

    def __init__(self, data: dict, user_id: int, domain_path: str):
        """
        任务数据格式处理
        fields = ('if_setup', 'exe_step', 'header_data', 'exe_data', 'result_data', 'created_by', 'updated_by')
        :param data: 需要添加的信息
        :param username: 用户名密码
        :return:
        """
        # 测试任务数据创建
        self.job_data = {
            'job_name': data['job_name'],
            'job_state': 10,
            'domain_path': domain_path,
            'autograph_config': str(data['autograph_config']),
            'header_data': str(data['config_info']),
            'global_list': str(data['global_list']),
        }
        # 测试任务数据外键
        self.job_context = {
            'created_by_id': user_id,
            'updated_by_id': user_id,
            'pro_id': data['job_pro'],
            'job_type': data['job_type']
        }
        # 测试任务数据详细
        self.case_list = []
        for case in data['case_info']:
            info = {
                # 'header_data': str(data['config_info']),
                'exe_data': case['exe_data'],
                'if_setup': 0,
                'exe_step': case['exe_order'],
                'domain_path': "",
                # 'save_list': case['save_params'],
                'save_list': '',
                # 'created_by': username,
                # 'updated_by': username
            }
            context = {
                'created_by_id': user_id,
                'updated_by_id': user_id,
                'case_id': case['case_id'],
            }
            self.case_list.append({'data': info, 'context': context})
        # 前提条件数据详细
        self.setup_list = []
        for setup in data['setup_list']:
            info = {
                # 'header_data': str(data['config_info']),
                'exe_data': setup['exe_data'],
                'if_setup': 1,
                'exe_step': setup['exe_order'],
                'domain_path': "",
                # 'save_list': setup['save_params'],
                'save_list': '',
                # 'created_by': username,
                # 'updated_by': username
            }
            context = {
                'created_by_id': user_id,
                'updated_by_id': user_id,
                'case_id': setup['case_id'],
            }
            self.setup_list.append({'data': info, 'context': context})

    def createJob(self):
        """
        根据数据创建任务
        :return:
        """
        try:
            # 创建任务信息
            new_job = JobInfoSerializer(data=self.job_data, context=self.job_context)
            new_job.is_valid(raise_exception=True)
            job_into = new_job.save()
            job_id = job_into.id
            # 补充任务信息，并添加任务信息id进入任务数据表
            for case in self.case_list:
                info = case['context']
                info['job_id'] = job_id
                new_case = JobDataSerializer(data=case['data'], context=case['context'])
                new_case.is_valid(raise_exception=True)
                new_case.save()
            for setup in self.setup_list:
                info = setup['context']
                info['job_id'] = job_id
                new_setup = JobDataSerializer(data=setup['data'], context=setup['context'])
                new_setup.is_valid(raise_exception=True)
                new_setup.save()
            return {'state': 200, 'data': job_id}
        except Exception as ex:
            return {'state': 110, 'data': ex}
