#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

from django.db import transaction

from rest_framework.views import APIView

from PlatApp.FunctionsForModels.TestCaseFunctions import RequestCaseData
from common.ReturnJson import ReturnJson

from PlatApp.models import CaseInfoForCaseCenter, CaseSuiteForCaseCenter, BaseSysParam, CaseStepForCaseCenter
from PlatApp.SerializersForModel.CaseSerializer import CaseInfoListSerializer, CaseSuiteListSerializer
from PlatApp.RestFulForApp.PageRestFul import GoodsPagination
from PlatApp.CustomizeEnumeration.CaseEnumerations import CaseEnumeration

logger = logging.getLogger('AutoApp.app')


class CaseInfoApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 获取测试用例列表
    """
    @transaction.atomic
    def post(self, requests):
        """
        创建测试用例
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("新增的用例信息为: {}".format(data))
        user = requests.user.username
        logger.info("创建人为: {}".format(user))
        sid = transaction.savepoint()
        try:
            # 拼接测试用例信息数据
            case_info = {
                'case_name': data['case_name'],
                'description': data['description'],
                'created_by': user,
                'updated_by': user,
            }
            context = {
                'pro_id': data['project_id'],
                'case_type': data['case_type_id']
            }
            # 创建测试用例信息数据
            data_obj = RequestCaseData()
            case_result = data_obj.CreateCaseInfo(data=case_info, context=context)
            try:
                case_id = case_result.id
            except Exception as ex:
                logger.error(ex)
                logger.error(case_result)
                transaction.rollback(sid)
                return ReturnJson.faile(CaseEnumeration.CREATE_CASE_INFO_ERROR.value)
            # 循环获取测试步骤列表进行创建
            step_id_list = []
            for step in data['case_step']:
                # 处理请求和相应参数
                execute_info_list = step['execute_info']
                for execute_info in execute_info_list:
                    if isinstance(execute_info, dict):
                        del execute_info['LAY_TABLE_INDEX']

                param_info_list = step['param_info']
                for param_info in param_info_list:
                    if isinstance(param_info, dict):
                        del param_info['LAY_TABLE_INDEX']
                # 拼接测试用例步骤数据
                step_info = {
                    'case': case_id,
                    'step_type': 'execute',
                    'step_id': step['step_id'],
                    'execute_type': 'HTTP',
                    'for_id': step['re_id'],
                    'check_type': 10,
                    'save_list': step['save_list'],
                    'execute_info': str(execute_info_list),
                    'param_info': str(param_info_list),
                    'description': data['case_name'],
                    'created_by': user,
                    'updated_by': user,
                }
                # 创建测试用例步骤数据
                step_result = data_obj.CreateCaseStep(step_info, 'case')
                try:
                    step_id = step_result.id
                    step_id_list.append(step_id)
                except Exception as ex:
                    logger.error(ex)
                    logger.error(step_result)
                    transaction.rollback(sid)
                    return ReturnJson.faile(CaseEnumeration.CREATE_CASE_STEP_ERROR.value)

            for id in step_id_list:
                case_result.step_list.add(id)
                case_result.save()

            transaction.savepoint_commit(sid)
            return ReturnJson.success(case_id)
        except Exception as e:
            transaction.rollback(sid)
            logger.error("新增接口信息失败: {}".format(e))
            return ReturnJson.faile(CaseEnumeration.CREATE_CASE_ERROR.value)

    def get(self, request):
        """
        获取测试用例列表
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("获取测试用例列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                data['pro__parent__id__in'] = eval(data['pro__parent__id__in'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]

                roles = CaseInfoForCaseCenter.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = CaseInfoListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = CaseInfoForCaseCenter.objects.get_queryset().order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = CaseInfoListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(CaseEnumeration.GET_INFO_ERROR.value)

    @transaction.atomic
    def put(self, requests):
        """
        更新测试用例数据状态
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("更新的测试用例信息为: {}".format(data))
        user_id = requests.user.id
        logger.info("更新人为: {}".format(user_id))
        try:
            if not data.__contains__('data_id') or data['data_id'] == '':
                return ReturnJson.faile(CaseEnumeration.GET_INFO_ERROR.value)
            logger.info("查找测试用例数据并更新")
            data_obj = CaseInfoForCaseCenter.objects.get(id=int(data['data_id']))
            sid = transaction.savepoint()
            if data_obj:

                if data.__contains__('case_name'):
                    data_obj.case_name = data['case_name']
                if data.__contains__('if_update'):
                    data_obj.if_update = data['if_update']
                if data.__contains__('description'):
                    data_obj.description = data['description']
                if data.__contains__('pro_id'):
                    data_obj.pro_id = int(data['pro_id'])
                if data.__contains__('abandon_flag'):
                    data_obj.abandon_flag = int(data['abandon_flag'])
                if data.__contains__('case_type_id'):
                    data_obj.case_type_id = int(data['case_type_id'])
                if data.__contains__('case_suite_id'):
                    data_obj.case_suite_id = int(data['case_suite_id'])
                data_obj.updated_by_id = user_id
                data_obj.save()
                if data.__contains__('abandon_flag'):
                    logger.error("更新内容有数据状态，开始更新测试步骤状态")
                    try:
                        CaseStepForCaseCenter.objects.filter(case=int(data['data_id'])).update(
                            abandon_flag=data['abandon_flag'], updated_at=time.strftime('%Y-%m-%d %H:%M:%S'),
                            updated_by_id=user_id)
                    except Exception as e:
                        logger.error("更新测试步骤状态失败: {}".format(e))
                        return ReturnJson.faile(CaseEnumeration.UPDATE_CASE_STEP_ERROR.value)
                    logger.info("状态更新成功")
                transaction.savepoint_commit(sid)
                return ReturnJson.success("状态更新成功")
            else:
                transaction.savepoint_rollback(sid)
                logger.error("更新测试用例状态失败，用例不存在")
                return ReturnJson.faile(CaseEnumeration.UPDATE_CASE_ERROR.value)

        except Exception as e:
            logger.error("更新测试用例状态失败: {}".format(e))
            return ReturnJson.faile(CaseEnumeration.UPDATE_CASE_ERROR.value)


class CaseSuiteApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 获取测试集合列表
    """

    def get(self, request):
        """
        获取测试集合列表
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("获取测试集合列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                data['pro__parent__id__in'] = eval(data['pro__parent__id__in'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]

                roles = CaseSuiteForCaseCenter.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = CaseSuiteListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = CaseSuiteForCaseCenter.objects.get_queryset().order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = CaseSuiteListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(CaseEnumeration.GET_INFO_ERROR.value)

    @transaction.atomic
    def put(self, requests):
        """
        更新测试集合数据状态
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("更新的测试集合信息为: {}".format(data))
        user = requests.user.username
        logger.info("更新人为: {}".format(user))
        try:
            logger.info("查找测试集合数据并更新")
            suite_obj = CaseSuiteForCaseCenter.objects.get(id=int(data['data_id']))
            sid = transaction.savepoint()

            if suite_obj:
                suite_obj.abandon_flag = data['abandon_flag']
                suite_obj.save()
                case_list = suite_obj.case_id.all()
                case_id_list = [int(info.id) for info in case_list]
                try:
                    CaseInfoForCaseCenter.objects.filter(id__in=case_id_list)\
                        .update(abandon_flag=data['abandon_flag'], updated_at=time.strftime('%Y-%m-%d %H:%M:%S'), updated_by=user)
                    try:
                        CaseStepForCaseCenter.objects.filter(case__in=case_id_list)\
                            .update(abandon_flag=data['abandon_flag'], updated_at=time.strftime('%Y-%m-%d %H:%M:%S'), updated_by=user)
                    except Exception as e:
                        logger.error("更新测试步骤状态失败: {}".format(e))
                        transaction.savepoint_rollback(sid)
                        return ReturnJson.faile(CaseEnumeration.UPDATE_CASE_STEP_ERROR.value)
                except Exception as e:
                    transaction.savepoint_rollback(sid)
                    logger.error("更新测试用例状态失败: {}".format(e))
                    return ReturnJson.faile(CaseEnumeration.UPDATE_CASE_ERROR.value)
                logger.info("状态更新成功")
                transaction.savepoint_commit(sid)
                return ReturnJson.success("状态更新成功")
            else:
                transaction.savepoint_rollback(sid)
                logger.error("更新测试集合状态失败，集合不存在")
                return ReturnJson.faile(CaseEnumeration.UPDATE_SUITE_ERROR.value)

        except Exception as e:
            logger.error("更新测试集合状态失败: {}".format(e))
            return ReturnJson.faile(CaseEnumeration.UPDATE_SUITE_ERROR.value)