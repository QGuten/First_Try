# -*- coding: utf-8 -*-
import logging
import datetime
import json

from django.forms import model_to_dict
from rest_framework.views import APIView
from django.db import transaction
from django.core import serializers

from common.ReturnJson import ReturnJson
from common.RandomForToken import GetCode

from AutoTest.InterfaceDocument.functions.GetDocsInfo import GetDocsInfoForUrl

from PlatApp.RestFulForApp.PageRestFul import GoodsPagination

from PlatApp.FunctionsForModels.TestCaseCreateFunctions import CreateTestCase
from PlatApp.SerializersForModel.BaseSerializer import JobRecordForBaseSerializer
from PlatApp.CustomizeEnumeration.ResourceEnumerations import *
from PlatApp.SerializersForModel.ResourcesSerializer import ConfigForResourcesSerializer, \
    RequestsForResourcesSerializer, RequestsListSerializer, GetConfigForResourcesSerializer
from PlatApp.models import ConfigForResources, ProjectForBase, JobRecordForBase, RequestsForResources, BaseSysParam

logger = logging.getLogger('AutoApp.app')


class ConfigApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 获取配置管理列表
    """
    def post(self, request):
        """
        post方法，添加配置
        :return:
        """
        logger.info('开始执行资源库添加配置接口')
        data = request.data
        user_id = request.user.id
        logger.info(str(data))
        try:
            context = {
                "pro_id": data["pro_id"],
                'created_by_id': user_id,
                'updated_by_id': user_id,
            }
            if ConfigForResources.objects.filter(key=data['key'], value=data['value'], pro_id=int(data["pro_id"])):
                logger.error("新增资源库添加配置失败: {}".format(ResourceEnumeration.CONFIG_REPEAT_ERROE.value))
                return ReturnJson.faile(ResourceEnumeration.CONFIG_REPEAT_ERROE.value)
            # 使用序列化创建数据
            new_config = ConfigForResourcesSerializer(data=data, context=context)
            new_config.is_valid(raise_exception=True)
            new_config.save()
            logger.info('资源库新增配置成功')
            return ReturnJson.success('资源库新增配置成功')
        except Exception as ex:
            logger.error("新增资源库添加配置失败: {}".format(ex))
            return ReturnJson.faile(ResourceEnumeration.CREATE_CONFIG_ERROE.value)

    def put(self, request):
        """
        put方法，更新配置
        :return:
        """
        logger.info('开始执行更新配置接口')
        data = request.data
        user_id = request.user.id
        logger.info(str(data))
        try:
            if not data.__contains__('config_id') or data['config_id'] == '':
                return ReturnJson.faile(ResourceEnumeration.CONFIG_ID_ERROR.value)
            config_info = ConfigForResources.objects.filter(id=int(data['config_id'])).first()
            if data.__contains__('key'):
                if ConfigForResources.objects.filter(key=data['key'], value=data['value'], pro_id=int(data["pro_id"])).exclude(id=int(data['config_id'])):
                    logger.error("更新资源库添加配置失败: {}".format(ResourceEnumeration.CONFIG_REPEAT_ERROE.value))
                    return ReturnJson.faile(ResourceEnumeration.CONFIG_REPEAT_ERROE.value)
                config_info.key = data['key']
            if data.__contains__('value'):
                if ConfigForResources.objects.filter(key=data['key'], value=data['value'], pro_id=int(data["pro_id"])).exclude(id=int(data['config_id'])):
                    logger.error("更新资源库添加配置失败: {}".format(ResourceEnumeration.CONFIG_REPEAT_ERROE.value))
                    return ReturnJson.faile(ResourceEnumeration.CONFIG_REPEAT_ERROE.value)
                config_info.value = data['value']
            if data.__contains__('name'):
                config_info.name = data['name']
            if data.__contains__('description'):
                config_info.description = data['description']
            if data.__contains__('pro_id'):
                config_info.pro_id = int(data['pro_id'])
            if data.__contains__('abandon_flag'):
                config_info.abandon_flag = int(data['abandon_flag'])
            config_info.updated_by_id = user_id
            config_info.save()
        except Exception as ex:
            logger.error("更新资源库添加配置失败: {}".format(ex))
            return ReturnJson.faile(ResourceEnumeration.UPDATE_CONFIG_ERROE.value)
        else:
            logger.info('更新配置成功')
            return ReturnJson.success('更新成功')

    def get(self, request):
        """
        获取配置管理列表
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("获取配置管理列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                data['pro__id__in'] = eval(data['pro__id__in'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]

                roles = ConfigForResources.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = GetConfigForResourcesSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = ConfigForResources.objects.get_queryset().order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = GetConfigForResourcesSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(ResourceEnumeration.GET_REQUEST_LIST_ERROE.value)


class RequestsApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 接口信息相关表结构
    """

    @transaction.atomic
    def post(self, requests):
        """
        新增接口信息
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("新增的接口信息为: {}".format(data))
        user_id = requests.user.id
        logger.info("创建人为: {}".format(user_id))
        serial_number = GetCode()
        data['serial_number'] = serial_number
        data['abandon_flag'] = 1
        data['ex_response'] = ""
        param_list = ['re_name', 're_path', 're_method', 'developer', 'project_id',
                      're_params', 're_response', 'description', 'if_case', 'edition']

        logger.info("开始检测请求参数")
        for param in param_list:
            if data.__contains__(param):
                continue
            else:
                logger.error("新增接口信息失败: {}".format("请求参数错误"))
                return ReturnJson.faile(ResourceEnumeration.CONFIG_ID_ERROR.value)
        logger.info("请求参数检测通过")

        logger.info("开始检测接口信息")
        if RequestsForResources.objects.filter(re_path=data['re_path'], re_method=data['re_method'], abandon_flag=1):
            logger.error("新增接口信息失败: {}".format("该接口地址已经添加，请勿重复添加！"))
            return ReturnJson.faile(ResourceEnumeration.RE_PATH_ERROR.value)
        logger.info("接口地址检测信息")

        try:
            logger.info("开始新增接口信息")
            context = {
                "project_id": int(data['project_id']),
                'created_by_id': user_id,
                'updated_by_id': user_id,
            }
            new_apiinfo = RequestsForResourcesSerializer(data=data, context=context)
            new_apiinfo.is_valid(raise_exception=True)
            apiinfo = new_apiinfo.save()
            logger.info("新增成功，判断是否生成测试用例")
            if data['if_case'] == '1':
                sid = transaction.savepoint()
                logger.info('需要生成测试用例，开始执行')
                data['id'] = apiinfo.id
                # 拼接生成测试用例方法的参数
                case_info = {'case_type': data['case_type'], 're_id': apiinfo.id}
                # 通过方法，生成测试用例数据
                info = CreateTestCase(data, case_info, user_id)
                result = info.CreateTestCaseData()
                # 判断测试用例是否生成成功
                if result['status'] == 110:
                    logger.info("测试用例生成失败")
                    logger.error(result['errorMsg'])
                    transaction.savepoint_commit(sid)
                    return ReturnJson.faile(ResourceEnumeration.CREATE_CASE_ERROR.value)
                else:
                    re_data = RequestsForResources.objects.get(id=apiinfo.id)
                    re_data.if_have_case = 0
                    re_data.save()
                    logger.info("测试用例生成成功")
                    return ReturnJson.success(int(apiinfo.id))
            else:
                return ReturnJson.success(int(apiinfo.id))
        except Exception as e:
            logger.error("新增接口信息失败: {}".format(e))
            return ReturnJson.faile(ResourceEnumeration.CREATE_REQUEST_ERROR.value)

    @transaction.atomic
    def put(self, requests):
        """
        更新接口信息
        :param requests:
        :return:
        """
        data = requests.data
        logger.info("更新的接口信息为: {}".format(data))
        user_id = requests.user.id
        logger.info("创建人为: {}".format(user_id))
        logger.info('开始校验请求参数')
        if data.__contains__('abandon_flag'):
            try:
                logger.info("查找接口信息数据并更新")
                data_obj = RequestsForResources.objects.get(id=data['data_id'])
                if data_obj:
                    data_obj.abandon_flag = data['abandon_flag']
                    data_obj.updated_by_id = user_id
                    data_obj.save()
                    logger.info("状态更新成功")
                    return ReturnJson.success("状态更新成功")
                else:
                    logger.error("更新接口数据状态失败，接口不存在")
                    return ReturnJson.faile(ResourceEnumeration.REQUEST_ID_ERROR.value)

            except Exception as e:
                logger.error("更新接口数据状态失败: {}".format(e))
                return ReturnJson.faile(ResourceEnumeration.CREATE_REQUEST_ERROR.value)
        else:
            param_list = ['re_id', 're_num', 're_name', 're_path', 're_method', 'developer', 'project_id',
                          're_params', 're_response', 'description', 'edition']
            for param in param_list:
                if param_list.__contains__(param):
                    continue
                else:
                    logger.error("更新接口信息失败: {}".format("请求参数错误"))
                    return ReturnJson.faile(ResourceEnumeration.CONFIG_ID_ERROR.value)
            logger.info('参数校验通过')

            try:
                logger.info('开始处理接口数据')
                api_info = RequestsForResources.objects.get(id=int(data['re_id']))
                contrast_data_list = ['re_name', 're_path', 're_method', 'developer', 'project_id',
                                      're_params', 're_response', 'description', 'edition']

                if_add_new = 0

                for contrast_data in contrast_data_list:

                    if contrast_data == 'project_id':

                        if int(data[contrast_data]) == api_info.project_id:
                            continue
                        else:
                            if_add_new = 1

                    elif data[contrast_data] == model_to_dict(api_info)[contrast_data]:
                        continue
                    else:
                        if_add_new = 1

                if if_add_new == 1:

                    if RequestsForResources.objects.filter(re_path=data['re_path'], re_method=data['re_method'],
                                                           abandon_flag=1).exclude(id=int(data['re_id'])):
                        logger.error("更新接口信息失败: {}".format("该接口地址已经添加，请勿重复添加！"))
                        return ReturnJson.faile(ResourceEnumeration.RE_PATH_ERROR.value)

                    sid = transaction.savepoint()

                    logger.info('接口数据有变更，开始新增接口处理')

                    # 拼接数据
                    data['abandon_flag'] = 1
                    context = {
                        "project_id": int(data['project_id']),
                        'created_by_id': user_id,
                        'updated_by_id': user_id,
                    }
                    # 原接口数据逻辑删除
                    logger.info('逻辑删除原数据')
                    api_info.abandon_flag = 0
                    api_info.save()
                    logger.info('逻辑删除原数据成功')

                    logger.info('开始新增接口数据')
                    # 创建新接口数据
                    new_apiinfo = RequestsForResourcesSerializer(data=data, context=context)
                    new_apiinfo.is_valid(raise_exception=True)
                    a = new_apiinfo.save()
                    logger.info('新接口数据添加成功')

                    transaction.savepoint_commit(sid)
                    logger.info('接口信息更新成功')
                    return ReturnJson.success({'id': int(a.id), 'msg': '接口信息更新成功'})
                else:
                    logger.info('接口数据无变更，无须变化')
                    return ReturnJson.success({'id': int(data['re_id']), 'msg': '接口数据无变更，无须变化'})
            except Exception as e:
                logger.error("新增接口信息失败: {}".format(e))
                return ReturnJson.faile(ResourceEnumeration.UPDATE_REQUEST_ERROR.value)

    def get(self, request):
        """
        获取接口列表
        :param request:
        :return:
        """

        # 搜索数据
        # data = request.data
        # logger.info("搜索数据:{}".format(data))
        data = request.GET.get('search_data')
        logger.info("获取接口列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                if data.__contains__('project__parent__id__in'):
                    data['project__parent__id__in'] = eval(data['project__parent__id__in'])
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = RequestsForResources.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = RequestsListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                # roles = RequestsForResources.objects.get_queryset().order_by('-id').filter(abandon_flag=1)
                roles = RequestsForResources.objects.order_by('-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = RequestsListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(ResourceEnumeration.SYS_ERROE.value)


class GetRequestsDocsForUrl(APIView):
    """
    @Author: 朱孟彤
    @desc: 触发接口文档解析功能
    """

    @transaction.atomic
    def post(self, request):
        """
        post 方法，触发接口文档解析功能
        :param request:
        :return:
        """
        logger.info('开始执行接口文档解析接口')
        data = request.data
        username = request.user.username
        logger.info(str(data))
        # 拼接任务执行记录数据
        info = {
            "params": str(data),
            "created_by": username,
            "updated_by": username,
            "state": 10, "date": "", "explain": "", "description": ""
        }
        # logger.info(str(info))
        job_id = ''
        all_info_list = []
        exe_num = []
        try:
            logger.info("创建一个接口文档解析的系统任务执行记录")
            add_record = JobRecordForBaseSerializer(data=info, context={"job_id": data["job_id"]})
            add_record.is_valid(raise_exception=True)
            job_info = add_record.save()
            # 任务执行记录id
            job_id = job_info.id
            logger.info("根据前端传输过来的配置id，获取配置中的地址url，以及所属项目的项目id")
            config_id_list = [int(x) for x in data['config_id']]  # 利用列表生成式，转换列表中元素的类型
            # 查询id在前端传输过来的参数 config_id中的所有配置信息列表，用来获取接口文档地址
            config_info = ConfigForResources.objects.filter(id__in=config_id_list)
            logger.info("更新任务执行记录的任务状态")
            # 任务开始执行，更新任务状态
            record_info = JobRecordForBase.objects.get(id=job_id)
            record_info.state = 20
            record_info.save()
            sid = transaction.savepoint()
            logger.info("根据url获取数据")
            for config in config_info:
                logger.info(config)
                logger.info("数据处理，入库")
                logger.info("循环url列表，获取数据")
                # 解析文档类，实例化对象
                info = GetDocsInfoForUrl()
                logger.info(str(config.value))
                logger.info("开始获取文档中的数据，请等待……")
                pro_id = config.pro_id
                # 根据接口文档地址，开始解析接口文档
                all_info = info.getDocsInfo(config.value)
                # 通过返回值判断是否解析成功
                if all_info['status'] == 110:
                    logger.error("接口文档详情解析失败")
                    transaction.savepoint_commit(sid)
                    record_info = JobRecordForBase.objects.get(id=job_id)
                    record_info.state = 110
                    record_info.date = str(all_info_list)
                    record_info.save()
                    # transaction.rollback(sid)
                    return ReturnJson.faile(ResourceEnumeration.GET_RE_DOCS_ERROR.value)
                all_info_list.append(all_info['data'])
                exe_num.append(all_info['exe_info'])
                logger.info("数据获取成功")
                # logger.info(str(all_info))
                # 获取数据中的所有模块
                models = all_info['data'].keys()
                logger.info(str(models))
                for model in models:
                    # 循环获取解析出的模块，判断模块是否存在，若不存在，则添加
                    logger.info("1.先处理数据中获取到的模块，若模块不存在，则需要在项目配置中新增一条记录")
                    info = ProjectForBase.objects.filter(project_name=model)
                    if info:
                        logger.info("模块存在")
                        model_id = info.first().id
                    else:
                        logger.info("模块不存在，新增一个模块")
                        new_pro = ProjectForBase()
                        new_pro.project_name = model
                        new_pro.project_type = "模块"
                        new_pro.parent_id = int(pro_id)
                        new_pro.save()
                        model_id = new_pro.id
                    logger.info("2.开始处理接口数据，添加数据到数据库")
                    logger.info(model_id)
                    # 添加解析出的接口文档数据添加至数据库
                    a = all_info['data']
                    requests_list = a[model]
                    for request_info in requests_list:
                        add_data = {'serial_number': GetCode(6),
                                    'project_id': model_id,
                                    'created_by': username,
                                    'updated_by': username,
                                    }
                        # 判断每一种字段不存在或为空的情况
                        if request_info.__contains__('DeveloperName'):
                            add_data["developer"] = str(request_info.pop('DeveloperName'))
                        else:
                            add_data["developer"] = "无"

                        if request_info.__contains__('docs_path'):
                            add_data["docs_path"] = str(request_info.pop('docs_path'))
                        else:
                            add_data["re_method"] = "无"
                        if request_info.__contains__('RequestName'):
                            add_data["re_name"] = str(request_info.pop('RequestName'))
                        else:
                            add_data["re_name"] = "无"
                        if request_info.__contains__('接口地址'):
                            add_data["re_path"] = str(request_info.pop('接口地址'))
                        else:
                            add_data["re_path"] = "无"
                        if request_info.__contains__('请求方式'):
                            add_data["re_method"] = str(request_info.pop('请求方式'))
                        else:
                            add_data["re_method"] = "无"
                        if request_info.__contains__('请求参数'):
                            add_data["re_params"] = str(request_info.pop('请求参数'))
                        else:
                            add_data["re_params"] = "无"
                        if request_info.__contains__('响应参数'):
                            add_data["re_response"] = str(request_info.pop('响应参数'))
                        else:
                            add_data["re_response"] = "无"
                        if request_info.__contains__('响应示例'):
                            add_data["ex_response"] = str(request_info.pop('响应示例'))
                        else:
                            add_data["ex_response"] = "无"
                        if request_info.__contains__('错误示例'):
                            add_data["error_response"] = str(request_info.pop('错误示例'))
                        else:
                            add_data["error_response"] = "无"
                        add_data["edition"] = None
                        add_data["re_other"] = str(request_info)
                        logger.info(str(add_data))
                        # 序列化的方式添加接口数据
                        add_info = RequestsForResourcesSerializer(data=add_data, context={"project_id": int(model_id)})
                        add_info.is_valid(raise_exception=True)
                        re_info = add_info.save()
                        logger.info("添加接口数据成功，判断是否需要生成测试用例")
                        if data['if_case'] == '1':
                            logger.info('需要生成测试用例，开始执行')
                            add_data['id'] = re_info.id
                            # 拼接生成测试用例方法的参数
                            case_info = {'case_type': data['case_type'], 're_id': re_info.id}
                            # 通过方法，生成测试用例数据
                            info = CreateTestCase(add_data, case_info, username)
                            result = info.CreateTestCaseData()
                            # 判断测试用例是否生成成功
                            if result['status'] == 110:
                                logger.info("测试用例生成失败")
                                logger.error(result['errorMsg'])
                                transaction.savepoint_commit(sid)
                                record_info = JobRecordForBase.objects.get(id=job_id)
                                record_info.state = 110
                                record_info.date = str(all_info_list)
                                record_info.save()
                                return ReturnJson.faile(ResourceEnumeration.CREATE_CASE_ERROR.value)
                            logger.info("测试用例生成成功")
                    """
                    logger.info("根据接口地址判断接口数据是否存在")
                    logger.info("接口数据存在，则对比数据，更新状态")
                    logger.info("接口数据不存在，调用生成随机码方法，生成一个接口的唯一标识，并添加接口数据至数据库")
                    """
            logger.info("所有数据更新后，更新任务状态")
            record_info = JobRecordForBase.objects.get(id=job_id)
            record_info.explain = str(exe_num)
            record_info.state = 30
            record_info.date = str(all_info_list)
            record_info.save()
            logger.info("更新状态成功")
        except Exception as ex:
            logger.error(ex)
            # transaction.rollback(sid)
            record_info = JobRecordForBase.objects.get(id=job_id)
            record_info.state = 110
            record_info.date = str(all_info_list)
            record_info.save()
            return ReturnJson.faile(ResourceEnumeration.RE_ERROR.value)
        else:
            logger.info("接口执行正常，提交事务")
            transaction.savepoint_commit(sid)
            return ReturnJson.success('新增成功')


class RequestsToCase(APIView):
    """
    @Author: 朱孟彤
    @desc: 为接口数据创建测试用例
    """

    @transaction.atomic
    def post(self, request):
        """
        post方法，为接口数据创建测试用例
        :param request:
        :return:
        """
        logger.info('开始执行接口数据创建测试用例接口')
        data = request.data
        user_id = request.user.id
        logger.info(str(data))
        sid = transaction.savepoint()
        try:
            logger.info('获取接口数据')
            re_info = RequestsForResources.objects.get(id=int(data['re_id'])).__dict__
            # logger.info(str(re_info))
            info = CreateTestCase(re_info, data, user_id)
            result = info.CreateTestCaseData()
            if result['status'] == 110:
                logger.error(result['errorMsg'])
                transaction.rollback(sid)
                return ReturnJson.faile(ResourceEnumeration.CREATE_CASE_ERROR.value)
        except Exception as ex:
            logger.error(ex)
            transaction.rollback(sid)
            return ReturnJson.faile(ResourceEnumeration.CREATE_CASE_ERROR.value)
        else:
            logger.info("接口执行正常，提交事务")
            transaction.savepoint_commit(sid)
            re_data = RequestsForResources.objects.get(id=int(data['re_id']))
            re_data.if_have_case = 0
            re_data.save()
            return ReturnJson.success('新增成功')



