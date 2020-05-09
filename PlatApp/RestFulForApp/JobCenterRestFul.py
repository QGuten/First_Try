# -*- coding: utf-8 -*-
import datetime
import logging
import json
import time

from rest_framework.views import APIView

from django.db import transaction
from django.forms import model_to_dict
from django.core.cache import cache

from common.ReturnJson import ReturnJson
from common.RandomForToken import GetCode

from AutoTest.InterfaceDocument.functions.GetDocsInfo import GetDocsInfoForUrl

from PlatApp.FunctionsForModels.TestCaseCreateFunctions import CreateTestCase
from PlatApp.SerializersForModel.JobInfoSerializer import IterationSerializer, JobReportDetailSerializer, \
    IterationListSerializer, SubJobInfoListSerializer, SubJobDataSerializer, JobReportListSerializer, \
    IterationRecordSerializer, IterationListRecordSerializer
from PlatApp.CustomizeEnumeration.JobEnumeration import JobCenterEnumeration
from PlatApp.SerializersForModel.JobInfoSerializer import JobInfoListSerializer, JobReportListDeSerializer, \
    SubJobInfoSerializer, SubJobInfoListSerializer, JobReportInfoSerializer
from PlatApp.models import RequestsForResources, IterationForJobCenter, JobReportInfoForJobCenter, \
    IterationRecordForJobCenter
from PlatApp.models import CaseInfoForCaseCenter, CaseStepForCaseCenter, JobInfoForJobCenter, JobDataForJobCenter, \
    JobReportListForJobCenter, SubJobInfoForJobCenter, SubJobDataForJobCenter
from PlatApp.FunctionsForModels.TestJobFunctions import CreateJobData, ExeSubJob
from PlatApp.RestFulForApp.PageRestFul import GoodsPagination

from AutoTest.Src.runcase.RunInterface import RunInterface

logger = logging.getLogger('AutoApp.app')


class ExeJob(APIView):
    """
    @Author: 朱孟彤
    @desc: 执行任务
    """

    @transaction.atomic
    def post(self, requests):
        """
        post方法，执行任务
        :param requests:
        :return:
        """
        logger.info('开始执行 执行任务接口')
        data = requests.data
        # username = requests.user.username
        user_id = requests.user.id
        logger.info(str(data))
        job_id = data["job_id"]

        try:

            exe_obj = ExeSubJob()
            exe_result = exe_obj.exeSubJob(job_id, user_id)

            if exe_result['state'] == 110:

                return ReturnJson.faile(JobCenterEnumeration.EXE_SUB_JOB_ERROR.value)

            return ReturnJson.success("任务执行完毕，请在报告管理中，查看任务状态。")

        except Exception as ex:

            logger.error(ex)
            return ReturnJson.faile(JobCenterEnumeration.EXE_SUB_JOB_ERROR.value)

            # # 获取任务基础信息
            # logger.info("---> 开始获取任务基础信息")
            # job_info = SubJobInfoForJobCenter.objects.get(id=int(job_id))
            #
            # logger.info("---> 创建数据回滚节点")
            #
            # # 创建任务执行报告
            # logger.info("---> 拼接处理测试报告写入数据")
            #
            # report_info = {
            #     "case_count": '',
            #     "case_exe_count": '',
            #     "setup_count": '',
            #     "setup_exe_count": '',
            #     "report_name": str(job_info.job_name + '_' + start_at),
            #     "start_at": start_at
            # }
            # report_context = {
            #     "created_by_id": user_id,
            #     "updated_by_id": user_id,
            #     "job_id": job_id
            # }
            #
            # logger.info("---> 拼接数据完毕，开始创建测试报告数据")
            #
            # new_report = JobReportListSerializer(data=report_info, context=report_context)
            # new_report.is_valid(raise_exception=True)
            # new_report_info = new_report.save()
            # report_id = new_report_info.id
            #
            # logger.info("---> 添加测试报告信息至报告信息表成功")
            #
            # sid = transaction.savepoint()
            #
            # job_key = "case_job:" + str(job_id) + "_" + str(int(time.time())) + ":"
            # info_key = job_key + "job_info"
            # keys["job_info"] = info_key  # 任务基础信息key
            # cache.set(info_key, model_to_dict(job_info), timeout=9999999999)
            #
            # logger.info("---> 开始添加全局变量至缓存池")
            #
            # keys["cache_key"] = job_key + "params_cache"
            #
            # if job_info.global_list:
            #
            #     global_data_l = eval(job_info.global_list)
            #
            #     global_data = {}
            #
            #     for g_data in global_data_l:
            #         global_data.update(g_data)
            #
            #     cache.set(job_key + "params_cache", global_data, timeout=9999999999)
            #
            # logger.info("---> 开始添加全局变量至缓存池完毕")
            #
            # # 获取任务数据信息
            # logger.info("---> 开始获取任务数据信息")
            # job_data_list = SubJobDataForJobCenter.objects.filter(job_id=int(job_id))
            # logger.info("---> 获取任务数据信息成功")
            #
            # setup_list = []
            # case_list = []
            #
            # # 根据是否是前提条件获取数据
            # setup_dict = []
            # case_dict = []
            # logger.info("---> 开始根据任务数据信息，对任务数据信息进行处理，并添加数据至redis缓存")
            #
            # for job_data in job_data_list:
            #
            #     # # 请求域名
            #     # domain_path = job_data.domain_path
            #     # # 请求头
            #     # header_data = job_data.header_data
            #     # 请求数据
            #     exe_data = eval(job_data.exe_data)
            #     # 储存参数
            #     save_list = job_data.save_list
            #     # 步骤请求域名
            #     domain_path = job_data.domain_path
            #
            #     if job_data.if_setup:
            #         # 判断数据是否是前提条件
            #
            #         setup_keys = []
            #
            #         # key_header = job_key + "job_setup:" + str(job_data.exe_step)
            #         key_header = job_key + "job_setup:" + str(job_data.case_id)
            #
            #         # 根据case_id获取用例信息以及操作步骤列表
            #         case_info = CaseInfoForCaseCenter.objects.get(id=int(job_data.case_id))
            #
            #         a = case_info.step_list.all()  # 操作步骤列表
            #         step_list = [model_to_dict(i) for i in a]
            #
            #         case_info = model_to_dict(case_info)
            #         case_info['step_list'] = step_list
            #
            #         cache.set(key_header + ":case_info", case_info, timeout=9999999999)
            #
            #         # 获取接口id，并获取接口数据
            #         for data in exe_data:
            #             # for step in step_list:
            #             info = {}
            #             # exe_data 查找数据中，步骤id相同的数据一起存储
            #             # for data in exe_data:
            #             if len(step_list) == 1:
            #                 info.update(step_list[0])
            #                 if step_list[0]["execute_type"] == "HTTP":
            #                     info.update(
            #                         model_to_dict(RequestsForResources.objects.get(id=int(step_list[0]["for_id"]))))
            #                 # info['save_list'] = save_list
            #                 info['domain_path'] = domain_path
            #                 info["step_id"] = data['step_id']
            #                 # info["domain_path"] = domain_path
            #                 # info["header_data"] = header_data
            #                 # logger.info(data["data"])
            #                 # logger.info(type(data["data"]))
            #                 info.update(eval(data["data"]))
            #                 if not info.__contains__('save_list'):
            #                     info['save_list'] = save_list
            #             else:
            #                 # 多步骤，数据匹配，预留位置
            #                 pass
            #
            #             setup_key = key_header + ":" + str(info["step_id"]) + ":step_info"
            #             setup_keys.append({"info_key": setup_key})
            #             # case_keys.append(case_keys)
            #             # logger.info(str(info))
            #             cache.set(setup_key, info, timeout=9999999999)
            #
            #         setup_dict.append({"case_info": key_header + ":case_info", "step_keys": setup_keys})
            #
            #     else:
            #         # 若不是前提条件，那么数据为测试用例
            #         case_keys = []
            #
            #         # key_header = job_key + "job_case:" + str(job_data.exe_step)
            #         key_header = job_key + "job_case:" + str(job_data.case_id)
            #
            #         # 根据case_id获取用例信息以及操作步骤列表
            #         case_info = CaseInfoForCaseCenter.objects.get(id=job_data.case_id)
            #
            #         a = case_info.step_list.all()  # 操作步骤列表
            #         step_list = [model_to_dict(i) for i in a]
            #
            #         case_info = model_to_dict(case_info)
            #         case_info['step_list'] = step_list
            #
            #         cache.set(key_header + ":case_info", case_info, timeout=9999999999)
            #
            #         # 获取接口id，并获取接口数据
            #         for data in exe_data:
            #             # for step in step_list:
            #             info = {}
            #             # exe_data 查找数据中，步骤id相同的数据一起存储
            #             # for data in exe_data:
            #             if len(step_list) == 1:
            #                 info.update(step_list[0])
            #                 if step_list[0]["execute_type"] == "HTTP":
            #                     info.update(
            #                         model_to_dict(RequestsForResources.objects.get(id=int(step_list[0]["for_id"]))))
            #                 # info['save_list'] = save_list
            #                 info['domain_path'] = domain_path
            #                 info["step_id"] = data['step_id']
            #                 # info["domain_path"] = domain_path
            #                 # info["header_data"] = header_data
            #                 # logger.info(data["data"])
            #                 # logger.info(type(data["data"]))
            #                 info.update(eval(data["data"]))
            #                 if not info['save_list']:
            #                     info['save_list'] = save_list
            #             else:
            #                 # 多步骤，数据匹配，预留位置
            #                 pass
            #
            #             case_key = key_header + ":" + str(info["step_id"]) + ":step_info"
            #             case_keys.append({"info_key": case_key})
            #             # case_keys.append(case_keys)
            #             # logger.info(str(info))
            #             cache.set(case_key, info, timeout=9999999999)
            #
            #         case_dict.append({"case_info": key_header + ":case_info", "step_keys": case_keys})
            #
            # if len(setup_dict) != 0:
            #     setup_list.append(setup_dict)
            # if len(case_dict) != 0:
            #     case_list.append(case_dict)
            #
            # # keys["job_setup"] = setup_list
            # keys["job_setup"] = setup_dict
            # # keys["job_case"] = case_list
            # keys["job_case"] = case_dict
            # keys["job_keys"] = job_key + "key_list"
            #
            # cache.set(job_key + "key_list", keys, timeout=9999999999)
            #
            # logger.info("---> 任务数据信息获取、添加至redis缓存成功")
            #
            # logger.info("---> 任务开始执行")
            #
            # try:
            #
            #     run_connet = RunInterface()
            #
            #     result = run_connet.choice(keys)
            #
            #     logger.info(str(result))
            #
            #     logger.info("---> 任务执行结束")
            #
            # except Exception as ex:
            #     logger.error(ex)
            #     return ReturnJson.faile(JobCenterEnumeration.EXE_SUB_JOB_ERROR.value)
            #
            # logger.info("---> 开始添加测试报告相关信息")
            #
            # try:
            #
            #     logger.info("---> 更新测试报告，写入数据")
            #
            #     report_obj = JobReportListForJobCenter.objects.get(id=report_id)
            #
            #     report_obj.case_count = str(result['case_count'])
            #     report_obj.case_exe_count = str(result['case_step_count'])
            #     report_obj.setup_count = str(result['setup_count'])
            #     report_obj.setup_exe_count = str(result['setup_step_count'])
            #     report_obj.status = 20
            #
            #     report_obj.save()
            #
            #     logger.info("---> 更新执行结果统计至测试报告信息成功")
            #
            #     # 循环添加测试报告数据信息
            #     logger.info("---> 添加测试报告数据信息至报告详情表")
            #
            #     for setup in keys['job_setup']:
            #         # 添加前置条件结果信息
            #         case_info_cache = cache.get(setup['case_info'])
            #         if not setup.__contains__('exe_result'):
            #             break
            #         result_data_info = {
            #             "case_id": int(case_info_cache["id"]),
            #             "step_id": None,
            #             "exe_info": str(case_info_cache),
            #             "result_info": str(cache.get(setup['exe_result'])),
            #             "description": "前置条件结果信息",
            #         }
            #
            #         result_data_context = {
            #             "created_by_id": user_id,
            #             "updated_by_id": user_id,
            #             "report_id": report_id
            #         }
            #         new_case_data = JobReportInfoSerializer(data=result_data_info, context=result_data_context)
            #         new_case_data.is_valid(raise_exception=True)
            #         new_case_data.save()
            #         for step in setup["step_keys"]:
            #             step_info = cache.get(step['info_key'])
            #             step_data_info = {
            #                 "case_id": int(case_info_cache["id"]),
            #                 "step_id": int(step_info["step_id"]),
            #                 "exe_info": str(cache.get(step['exe_info_key'])),
            #                 "result_info": str(cache.get(step['result_key'])),
            #                 "description": str(case_info_cache),
            #             }
            #             step_data_context = {
            #                 "created_by_id": user_id,
            #                 "updated_by_id": user_id,
            #                 "report_id": report_id
            #             }
            #             new_step_data = JobReportInfoSerializer(data=step_data_info, context=step_data_context)
            #             new_step_data.is_valid(raise_exception=True)
            #             new_step_data.save()
            #
            #     for case in keys['job_case']:
            #         # 先添加执行用例结果信息
            #         case_info_cache = cache.get(case['case_info'])
            #         if not case.__contains__('exe_result'):
            #             break
            #         case_result_cache = cache.get(case['exe_result'])
            #         logger.info('测试用例执行结果：{}'.format(case_result_cache))
            #         result_data_info = {
            #             "case_id": int(case_info_cache["id"]),
            #             "step_id": None,
            #             "exe_info": str(case_info_cache),
            #             "result_info": case_result_cache,
            #             "description": "执行用例结果信息",
            #         }
            #         logger.info("测试用例结果信息：{}".format(result_data_info))
            #         result_data_context = {
            #             "created_by_id": user_id,
            #             "updated_by_id": user_id,
            #             "report_id": report_id
            #         }
            #         new_case_data = JobReportInfoSerializer(data=result_data_info, context=result_data_context)
            #         new_case_data.is_valid(raise_exception=True)
            #         new_case_data.save()
            #         for step in case["step_keys"]:
            #             step_info = cache.get(step['info_key'])
            #             step_data_info = {
            #                 "case_id": int(case_info_cache["id"]),
            #                 "step_id": int(step_info["step_id"]),
            #                 "exe_info": str(cache.get(step['exe_info_key'])),
            #                 "result_info": str(cache.get(step['result_key'])),
            #                 "description": str(case_info_cache),
            #             }
            #             step_data_context = {
            #                 "report_id": report_id,
            #                 "created_by_id": user_id,
            #                 "updated_by_id": user_id,
            #             }
            #             new_step_data = JobReportInfoSerializer(data=step_data_info, context=step_data_context)
            #             new_step_data.is_valid(raise_exception=True)
            #             new_step_data.save()
            #
            #     logger.info("---> 添加测试报告数据信息至报告详情表成功")
            #
            # except Exception as ex:
            #     logger.error(ex)
            #     transaction.rollback(sid)
            #     return ReturnJson.faile(JobCenterEnumeration.EXE_SUB_JOB_ERROR.value)
            #
            # logger.info("---> 任务执行成功，请在报告管理中，查看任务状态。")
            #
            # transaction.savepoint_commit(sid)
            #
            # logger.info("---> 任务执行结束，清除任务执行缓存。")
            #
            # if isinstance(keys, dict):
            #     for value in keys.values():
            #         if isinstance(value, list):
            #             for step_value in value:
            #                 if isinstance(step_value, dict):
            #                     for key_3 in step_value.values():
            #                         if isinstance(key_3, str):
            #                             cache.delete(key_3)
            #                         if isinstance(key_3, list):
            #                             for key_4 in key_3:
            #                                 if isinstance(key_4, dict):
            #                                     [cache.delete(key_5) for key_5 in key_4.values()]
            #         if isinstance(value, str):
            #             cache.delete(value)
            #
            # logger.info("---> 任务执行结束，清除任务执行缓存完毕。")
        #
        #     return ReturnJson.success("任务执行成功，请在报告管理中，查看任务状态。")
        #
        # except Exception as ex:
        #
        #     logger.error(ex)
        #     return ReturnJson.faile(JobCenterEnumeration.EXE_SUB_JOB_ERROR.value)


class ExeIterations(APIView):
    """
    @Author: 朱孟彤
    @desc: 执行迭代
    """

    @transaction.atomic
    def post(self, requests):
        """
        post方法，执行任务
        :param requests:
        :return:
        """
        logger.info('开始执行 执行迭代接口')
        data = requests.data
        # username = requests.user.username
        user_id = requests.user.id
        logger.info(str(data))

        try:
            if data.__contains__('it_id'):
                it_id = data["it_id"]
            else:
                return ReturnJson.faile(JobCenterEnumeration.GET_INFO_ERROR.value)

            re_data = {
                'description': '',
                'exe_overview': '',
            }
            re_context = {
                'created_by_id': user_id,
                'updated_by_id': user_id,
                'it_id': int(it_id),
            }

            it_record_obj = IterationRecordSerializer(data=re_data, context=re_context)
            it_record_obj.is_valid(raise_exception=True)
            record_obj = it_record_obj.save()

            it_obj = IterationForJobCenter.objects.get(id=int(it_id))
            job_list = it_obj.job.all()
            job_ids = [i.id for i in job_list]

            it_count = {'all_num': len(job_ids), 'fail_num': 0, 'pass_num': 0}

            report_ids = []

            for job_id in job_ids:

                exe_obj = ExeSubJob()
                # exe_obj.exeSubJob(job_id, user_id)
                exe_result = exe_obj.exeSubJob(job_id, user_id)

                if exe_result['state'] == 110:

                    it_count['fail_num'] += 1

                    # return ReturnJson.faile(JobCenterEnumeration.EXE_IT_JOB_ERROR.value)
                elif exe_result['state'] == 200:

                    report_ids.append(exe_result['data'])

                    it_count['pass_num'] += 1

            record_obj.report.add(*report_ids)
            record_obj.exe_overview = str(it_count)
            record_obj.updated_by_id = user_id
            record_obj.save()

            return ReturnJson.success("任务执行完毕，请在报告管理中，查看任务状态。")

        except Exception as ex:

            logger.error(ex)
            return ReturnJson.faile(JobCenterEnumeration.EXE_IT_JOB_ERROR.value)


class JobApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 测试任务相关接口
    """
    @transaction.atomic
    def post(self, requests):
        """
        post方法创建测试任务
        :param requests:
        :return:
        """
        logger.info('开始执行创建测试任务接口')
        data = requests.data
        # username = request.user.username
        user_id = requests.user.id
        logger.info(str(data))
        # 判断并获取请求头
        domain_path = data["domain_info"]
        sid = transaction.savepoint()
        addJob = CreateJobData(data, user_id, domain_path)
        result = addJob.createJob()
        if result['state'] == 110:
            logger.error(result['data'])
            transaction.rollback(sid)
            return ReturnJson.faile(JobCenterEnumeration.CREATE_JOB_ERROR.value)
        transaction.savepoint_commit(sid)
        return ReturnJson.success(int(result['data']))

    @transaction.atomic
    def put(self, requests):
        """
        更新父任务相关数据状态
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("更新的父任务信息为: {}".format(data))
        # user = requests.user.username
        user_id = requests.user.id
        logger.info("更新人为: {}".format(user_id))
        try:
            logger.info("查找父任务相关信息并更新")
            data_obj = JobInfoForJobCenter.objects.get(id=int(data['data_id']))
            sid = transaction.savepoint()
            if data_obj:
                data_obj.abandon_flag = data['abandon_flag']
                data_obj.save()
                try:
                    JobDataForJobCenter.objects.filter(job__id=int(data['data_id']))\
                        .update(abandon_flag=data['abandon_flag'], updated_at=time.strftime('%Y-%m-%d %H:%M:%S'), updated_by_id=user_id)
                    try:
                        sub_job_list = SubJobInfoForJobCenter.objects.filter(job__id=int(data['data_id']))
                        sub_job_list.update(abandon_flag=data['abandon_flag'], updated_at=time.strftime('%Y-%m-%d %H:%M:%S'), updated_by_id=user_id)
                        sub_job_id = [int(info.id) for info in sub_job_list]
                        try:
                            SubJobDataForJobCenter.objects.filter(job__id__in=sub_job_id)\
                                .update(abandon_flag=data['abandon_flag'], updated_at=time.strftime('%Y-%m-%d %H:%M:%S'), updated_by_id=user_id)
                        except Exception as e:
                            logger.error("更新子任务数据状态失败: {}".format(e))
                            transaction.savepoint_rollback(sid)
                            return ReturnJson.faile(JobCenterEnumeration.UPDATE_SUB_JOB_DATA_STATE_ERROR.value)
                    except Exception as e:
                        logger.error("更新子任务状态失败: {}".format(e))
                        transaction.savepoint_rollback(sid)
                        return ReturnJson.faile(JobCenterEnumeration.UPDATE_SUB_JOB_STATE_ERROR.value)
                except Exception as e:
                    logger.error("更新父任务数据状态失败: {}".format(e))
                    transaction.savepoint_rollback(sid)
                    return ReturnJson.faile(JobCenterEnumeration.UPDATE_JOB_DATA_STATE_ERROR.value)
                logger.info("状态更新成功")
                transaction.savepoint_commit(sid)
                return ReturnJson.success("状态更新成功")
            else:
                transaction.savepoint_rollback(sid)
                logger.error("更新父任务状态失败，父任务不存在")
                return ReturnJson.faile(JobCenterEnumeration.UPDATE_JOB_STATE_ERROR.value)
        except Exception as e:
            logger.error("更新父任务状态失败: {}".format(e))
            return ReturnJson.faile(JobCenterEnumeration.UPDATE_JOB_STATE_ERROR.value)

    def get(self, requests):
        """
        获取测试任务列表，包含查询
        :param requests:
        :return:
        """
        data = requests.GET.get('search_data')
        logger.info("获取测试任务列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                data['pro__id__in'] = eval(data['pro__id__in'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]

                roles = JobInfoForJobCenter.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 对查询数据进行序列化
                roles_ser = JobInfoListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = JobInfoForJobCenter.objects.get_queryset().order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 查询数据序列化处理
                roles_ser = JobInfoListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(JobCenterEnumeration.GET_INFO_ERROR.value)


class SubJobApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 测试子任务相关接口
    """

    @transaction.atomic
    def post(self, requests):
        """
        post方法创建测试任务
        :param requests:
        :return:
        """
        logger.info('开始执行创建测试子任务接口')
        data = requests.data
        # username = requests.user.username
        user_id = requests.user.id
        logger.info(str(data))

        # 根据任务id，获取父级任务的任务信息
        try:
            f_job_info = JobInfoForJobCenter.objects.values("job_name", "job_state", "pro_id", "job_type",
                                                            'global_list', 'domain_path', 'header_data',
                                                            'autograph_config').get(
                id=data["job_id"])
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(JobCenterEnumeration.GET_JOB_INFO_ERROR.value)

        sid = transaction.savepoint()
        try:
            # 根据父级任务的任务信息，添加父级任务的ID进入数据，新增子任务数据
            f_job_info["job_id"] = data["job_id"]
            f_job_info["domain_path"] = data["domain_path"]
            f_job_info["header_data"] = str(data["config_info"])
            f_job_info["global_list"] = str(data["global_list"])
            f_job_info["created_by_id"] = user_id
            f_job_info["updated_by_id"] = user_id
            f_job_info["job_name"] = data["job_name"]

            newSubJob = SubJobInfoSerializer(data=f_job_info, context=f_job_info)
            newSubJob.is_valid(raise_exception=True)
            SubJobInfo = newSubJob.save()

            # 处理子任务数据的数据，使其可以直接添加至子任务数据表
            # 测试任务数据详细
            for case in data['case_info']:
                info = {
                    'if_setup': 0,
                    # 'created_by_id': user_id,
                    # 'updated_by_id': user_id,
                    'save_list': ''
                }
                info.update(case)
                context = {
                    'created_by_id': user_id,
                    'updated_by_id': user_id,
                    'case_id': case['case_id'],
                    'job_id': SubJobInfo.id
                }
                new_JobData = SubJobDataSerializer(data=info, context=context)
                new_JobData.is_valid(raise_exception=True)
                new_JobData.save()

            # 前提条件数据详细

            for setup in data['setup_list']:
                info = {
                    'if_setup': 1,
                    # 'created_by': username,
                    # 'updated_by': username,
                    'save_list': ''
                }
                info.update(setup)
                context = {
                    'created_by_id': user_id,
                    'updated_by_id': user_id,
                    'job_id': SubJobInfo.id,
                    'case_id': setup['case_id'],
                }
                new_JobData = SubJobDataSerializer(data=info, context=context)
                new_JobData.is_valid(raise_exception=True)
                new_JobData.save()

        except Exception as ex:
            logger.error(ex)
            transaction.rollback(sid)
            return ReturnJson.faile(JobCenterEnumeration.CREATE_SUB_JOB_ERROR.value)

        else:
            transaction.savepoint_commit(sid)
            return ReturnJson.success(SubJobInfo.id)

    @transaction.atomic
    def put(self, requests):
        """
        更新子任务相关数据状态
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("更新的子任务信息为: {}".format(data))
        # user = requests.user.username
        user_id = requests.user.id
        logger.info("更新人为: {}".format(user_id))
        try:
            logger.info("查找子任务相关信息并更新")
            data_obj = SubJobInfoForJobCenter.objects.get(id=int(data['data_id']))

            sid = transaction.savepoint()

            if data_obj:

                logger.info("开始更新子任务信息")

                if data.__contains__('config_info'):
                    data_obj.header_data = str(data['config_info'])
                if data.__contains__('global_list'):
                    data_obj.global_list = str(data["global_list"])
                if data.__contains__('domain_path'):
                    data_obj.domain_path = data['domain_path']
                if data.__contains__('job_name'):
                    data_obj.job_name = data['job_name']
                if data.__contains__('autograph_config'):
                    data_obj.autograph_config = str(data["autograph_config"])
                if data.__contains__('abandon_flag'):
                    data_obj.abandon_flag = data['abandon_flag']

                    try:
                        SubJobDataForJobCenter.objects.filter(job_id=int(data['data_id'])).update(
                            abandon_flag=data['abandon_flag'], updated_at=time.strftime('%Y-%m-%d %H:%M:%S'),
                            updated_by_id=user_id)

                    except Exception as e:
                        logger.error("更新子任务数据状态失败: {}".format(e))
                        transaction.savepoint_rollback(sid)
                        return ReturnJson.faile(JobCenterEnumeration.UPDATE_SUB_JOB_DATA_STATE_ERROR.value)

                logger.info("子任务信息更新完毕")

                if data.__contains__('setup_list'):

                    setup_list = data['setup_list']

                    logger.info("开始更新前置条件信息")

                    for setup_info in setup_list:
                        setup_data = SubJobDataForJobCenter.objects.get(id=setup_info['data_id'])
                        setup_data.domain_path = setup_info['domain_path']
                        # setup_data.save_list = setup_info['save_list']
                        setup_data.exe_step = setup_info['exe_step']
                        # setup_data.header_data = setup_info['header_data']
                        setup_data.exe_data = setup_info['exe_data']
                        setup_data.updated_by_id = user_id
                        setup_data.save()

                    logger.info("前置条件信息更新完毕")

                if data.__contains__('case_info'):

                    logger.info("开始更新测试用例信息")

                    case_list = data['case_info']

                    for case_info in case_list:
                        case_data = SubJobDataForJobCenter.objects.get(id=case_info['data_id'])
                        case_data.domain_path = case_info['domain_path']
                        # case_data.save_list = case_info['save_list']
                        case_data.exe_step = case_info['exe_step']
                        # case_data.header_data = case_info['header_data']
                        case_data.updated_by_id = user_id
                        case_data.exe_data = case_info['exe_data']
                        case_data.save()

                    logger.info("测试用例信息更新完毕")

                data_obj.save()

                logger.info("状态更新成功")
                transaction.savepoint_commit(sid)
                return ReturnJson.success("状态更新成功")
            else:
                transaction.savepoint_rollback(sid)
                logger.error("更新子任务状态失败，子任务不存在")
                return ReturnJson.faile(JobCenterEnumeration.UPDATE_SUB_JOB_STATE_ERROR.value)

        except Exception as e:
            logger.error("更新子任务状态失败: {}".format(e))
            return ReturnJson.faile(JobCenterEnumeration.UPDATE_SUB_JOB_STATE_ERROR.value)

    def get(self, requests):
        """
        获取测试子任务列表，包含查询
        :param requests:
        :return:
        """
        data = requests.GET.get('search_data')
        job_id = requests.GET.get('job_id')
        logger.info("获取测试子任务列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                data['pro__id__in'] = eval(data['pro__id__in'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]

                roles = SubJobInfoForJobCenter.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 对查询数据进行序列化
                roles_ser = SubJobInfoListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = SubJobInfoForJobCenter.objects.filter(job_id=job_id).order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 查询数据序列化处理
                roles_ser = SubJobInfoListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(JobCenterEnumeration.GET_INFO_ERROR.value)


class IterationApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 迭代相关接口
    """
    def post(self, requests):
        """
        post，创建迭代接口
        :param requests:
        :return:
        """
        logger.info('开始执行创建迭代接口')
        data = requests.data
        # username = requests.user.username
        user_id = requests.user.id
        logger.info(str(data))
        try:
            info = {
                'name': data['name'],
                'state': 10,
                'description': data['description'],
            }
            context = {
                'created_by_id': user_id,
                'updated_by_id': user_id,
                'pro_id': int(data['pro_id']),
                'version_id': int(data['version_id'])
            }
            m_data = IterationSerializer(data=info, context=context)
            m_data.is_valid(raise_exception=True)
            data_obj = m_data.save()
            jobs = [int(r) for r in data['jobs']]
            data_obj.job.add(*jobs)
            return ReturnJson.success(int(data_obj.id))
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(JobCenterEnumeration.GET_JOB_INFO_ERROR.value)

    def put(self, requests):
        """
        修改迭代信息
        :param requests:
        :return:
        """
        logger.info('开始执行更新迭代信息接口')
        data = requests.data
        # username = requests.user.username
        user_id = requests.user.id
        logger.info(str(data))
        try:
            data_obj = IterationForJobCenter.objects.get(id=int(data['data_id']))

            if data.__contains__('name'):
                data_obj.name = data['name']
            if data.__contains__('state'):
                data_obj.state = data['state']
            if data.__contains__('description'):
                data_obj.description = data['description']
            if data.__contains__('pro_id'):
                data_obj.pro_id = int(data['pro_id'])
            if data.__contains__('version_id'):
                data_obj.version_id = int(data['version_id'])
            if data.__contains__('abandon_flag'):
                data_obj.abandon_flag = int(data['abandon_flag'])

            data_obj.updated_by_id = user_id
            data_obj.save()

            return ReturnJson.success(int(data_obj.id))
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(JobCenterEnumeration.UPDATE_IT_STATE_ERROR.value)

    def get(self, requests):
        """
        获取迭代列表，包含查询
        :param requests:
        :return:
        """
        data = requests.GET.get('search_data')
        logger.info("获取迭代列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                data['pro__id__in'] = eval(data['pro__id__in'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]

                roles = IterationForJobCenter.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 对查询数据进行序列化
                roles_ser = IterationListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = IterationForJobCenter.objects.get_queryset().order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 查询数据序列化处理
                roles_ser = IterationListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(JobCenterEnumeration.GET_INFO_ERROR.value)


class IterationRecordApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 迭代执行记录相关接口
    """

    def get(self, requests):
        """
        获取迭代执行记录，包含查询
        :param requests:
        :return:
        """
        data = requests.GET.get('search_data')
        logger.info("获取迭代执行列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                data['it__pro__id__in'] = eval(data['it__pro__id__in'])
                if data.__contains__('it__id'):
                    data['it_id'] = int(data['it_id'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = IterationRecordForJobCenter.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 对查询数据进行序列化
                roles_ser = IterationListRecordSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = IterationRecordForJobCenter.objects.get_queryset().order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 查询数据序列化处理
                roles_ser = IterationListRecordSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(JobCenterEnumeration.GET_INFO_ERROR.value)


class ReportApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 获取报告列表，包含查询
    """

    def get(self, requests):
        """
        获取报告列表，包含查询
        :param requests:
        :return:
        """
        data = requests.GET.get('search_data')
        logger.info("获取报告列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                data['job__pro__id__in'] = eval(data['job__pro__id__in'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = JobReportListForJobCenter.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 对查询数据进行序列化
                roles_ser = JobReportListDeSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = JobReportListForJobCenter.objects.get_queryset().order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=requests, view=self)
                # 查询数据序列化处理
                roles_ser = JobReportListDeSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(JobCenterEnumeration.GET_INFO_ERROR.value)


class SubJobDataInfoApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 根据子任务ID，获取测试用例执行数据
    """
    def post(self, requests):
        """
        根据子任务ID，获取测试用例执行数据
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("根据子任务ID，获取测试用例执行数据。{}".format(data))
        # user = requests.user.username
        user_id = requests.user.id
        logger.info("查询人为: {}".format(user_id))
        try:
            logger.info("开始查询用例执行信息")
            obj_data = SubJobDataForJobCenter.objects.filter(job_id=int(data['data_id']))
            result_data = []
            for i in obj_data:
                data = {}
                data.update(model_to_dict(i))
                data['case_name'] = i.case.case_name
                data['case_type'] = i.case.case_type.param_name
                result_data.append(data)
            return ReturnJson.success(result_data)
        except Exception as e:
            logger.error("查询用例执行信息失败: {}".format(e))
            return ReturnJson.faile(JobCenterEnumeration.GET_REPORT_CASE_INTO_ERROR.value)


class ReportDataInfoApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 根据用例ID和报告ID，获取测试用例步骤执行详情
    """

    def post(self, requests):
        """
        根据用例ID和报告ID，获取测试用例步骤执行详情
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("根据用例ID和报告ID，获取测试用例步骤执行详情。{}".format(data))
        # user = requests.user.username
        user_id = requests.user.id
        logger.info("查询人为: {}".format(user_id))
        try:
            logger.info("开始查询用例执行信息")
            result_data = JobReportInfoForJobCenter.objects.filter(case_id=int(data['case_id']),
                                                                   report_id=int(data['report_id'])).exclude(
                step_id__isnull=True)
            return ReturnJson.success([model_to_dict(re_data) for re_data in result_data])
        except Exception as e:
            logger.error("查询用例执行信息失败: {}".format(e))
            return ReturnJson.faile(JobCenterEnumeration.GET_REPORT_CASE_INTO_ERROR.value)