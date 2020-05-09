# -*- coding: utf-8 -*-
import logging

from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponseRedirect

from rest_framework.views import APIView

from common.ReturnJson import ReturnJson

from PlatApp.CustomizeEnumeration.BaseEnumeration import *
from PlatApp.models import ProjectForBase, BaseSysParam, VersionForProject
from PlatApp.SerializersForModel.BaseSerializer import BaseSysParamSerializer, BaseSysParamListSerializer, \
    ProjectListSerializer, VersionForProjectListSerializer, VersionForProjectSerializer, ProjectSerializer
from PlatApp.RestFulForApp.PageRestFul import GoodsPagination

from PlatApp.models import MDEditorForm
from PlatApp.FormsForApp.MDEditorForm import MDEditorModleForm

logger = logging.getLogger('AutoApp.app')


# @method_decorator(csrf_exempt, name='dispatch')
def WikiDocs(request):
    """
    @Author: 朱孟彤
    @desc: wiki
    """
    if request.method == 'POST':
        # if this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request:
        form = MDEditorModleForm(request.POST)
        logger.info(str(request.POST))
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            return HttpResponseRedirect('/BaseCenter/WikiDocsIndex/')
        else:
            return '11111'

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MDEditorModleForm()
    return render(request, 'index.html', {'form': form})


class SysParamApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 添加系统参数配置
    """

    def post(self, request):
        """
        post方法，添加系统参数配置
        :return:
        """
        logger.info('开始执行添加系统参数配置接口')
        data = request.data
        logger.info(str(data))
        user_id = request.user.id
        logger.info("新增数据：{}".format(data))
        try:
            context = {
                'created_by_id': user_id,
                'updated_by_id': user_id,
            }
            if BaseSysParam.objects.filter(param_key=data['param_key'], param_value=data['param_value']):
                logger.error("新增系统参数配置失败: {}".format(BaseEnumeration.CREATE_SYS_PARAM_REPEAT_ERROR.value))
                return ReturnJson.faile(BaseEnumeration.CREATE_SYS_PARAM_REPEAT_ERROR.value)
            new_sys = BaseSysParamSerializer(data=data, context=context)
            new_sys.is_valid(raise_exception=True)
            new_sys.save()
        except Exception as ex:
            logger.error("新增系统参数配置失败: {}".format(ex))
            return ReturnJson.faile(BaseEnumeration.CREATE_SYS_PARAM_ERROR.value)
        else:
            logger.info('新增系统参数配置成功')
            return ReturnJson.success('新增成功')

    def put(self, request):
        """
        put方法，更新系统参数配置
        :return:
        """
        logger.info('开始执行更新系统参数配置接口')
        data = request.data
        user_id = request.user.id
        logger.info(str(data))
        try:
            if not data.__contains__('sys_id') or data['sys_id'] == '':
                return ReturnJson.faile(BaseEnumeration.SYS_PARAM_ID_ERROR.value)
            sys_info = BaseSysParam.objects.get(id=int(data['sys_id']))
            if data.__contains__('param_key'):
                if BaseSysParam.objects.filter(param_key=data['param_key'], param_name=data['param_value']).exclude(id=int(data['sys_id'])):
                    logger.error("更新系统参数配置失败: {}".format(BaseEnumeration.CREATE_SYS_PARAM_REPEAT_ERROR.value))
                    return ReturnJson.faile(BaseEnumeration.CREATE_SYS_PARAM_REPEAT_ERROR.value)
                sys_info.param_key = data['param_key']
            if data.__contains__('param_value'):
                if BaseSysParam.objects.filter(param_key=data['param_key'], param_name=data['param_value']).exclude(id=int(data['sys_id'])):
                    logger.error("更新系统参数配置失败: {}".format(BaseEnumeration.CREATE_SYS_PARAM_REPEAT_ERROR.value))
                    return ReturnJson.faile(BaseEnumeration.CREATE_SYS_PARAM_REPEAT_ERROR.value)
                sys_info.param_value = data['param_value']
            if data.__contains__('param_name'):
                sys_info.param_name = data['param_name']
            if data.__contains__('description'):
                sys_info.description = data['description']
            if data.__contains__('abandon_flag'):
                sys_info.abandon_flag = int(data['abandon_flag'])
            sys_info.updated_by_id = user_id
            sys_info.save()
        except Exception as ex:
            logger.error("更新系统参数配置失败: {}".format(ex))
            return ReturnJson.faile(BaseEnumeration.UPDATE_SYS_PARAM_ERROR.value)
        else:
            logger.info('更新系统参数配置成功')
            return ReturnJson.success('更新成功')

    def get(self, request):
        """
        系统参数配置列表，列表和搜索
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("系统参数配置列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = BaseSysParam.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = BaseSysParamListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                # roles = BaseSysParam.objects.get_queryset().order_by('-id', 'abandon_flag')
                roles = BaseSysParam.objects.get_queryset().order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = BaseSysParamListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(BaseEnumeration.SYS_PARAM_ID_ERROR.value)


class ProjectApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 项目配置列表，列表和搜索
    """
    def post(self, request):
        """
        post方法，添加项目配置
        :return:
        """
        logger.info('开始执行添加项目配置接口')
        data = request.data
        logger.info(str(data))
        user_id = request.user.id
        try:
            if data.__contains__('parent_id'):
                context = {
                    'created_by_id': user_id,
                    'updated_by_id': user_id,
                    'parent_id': int(data['parent_id'])
                }
            else:
                context = {
                    'created_by_id': user_id,
                    'updated_by_id': user_id,
                }
            if ProjectForBase.objects.filter(project_name=data['project_name'], parent_id=int(data['parent_id'])):
                logger.error("新增项目配置失败: {}".format(BaseEnumeration.CREATE_PROJECT_DATA_ERROR.value))
                return ReturnJson.faile(BaseEnumeration.CREATE_PROJECT_DATA_ERROR.value)
            new_pro = ProjectSerializer(data=data, context=context)
            new_pro.is_valid(raise_exception=True)
            new_pro.save()
        except Exception as ex:
            logger.error(ex)
            logger.error(str(BaseEnumeration.CREATE_PROJECT_ERROR.value))
            return ReturnJson.faile(BaseEnumeration.CREATE_PROJECT_ERROR.value)
        else:
            logger.info('新增项目配置成功')
            return ReturnJson.success('新增成功')

    def put(self, request):
        """
        post方法，更新项目配置
        :return:
        """
        logger.info('开始执行更新项目配置接口')
        data = request.data
        logger.info(str(data))
        user_id = request.user.id
        try:
            if not data.__contains__('project_id') or data['project_id'] == '':
                return ReturnJson.faile(BaseEnumeration.PROJECT_ID_ERROR.value)

            pro_info = ProjectForBase.objects.get(id=int(data['project_id']))

            if data.__contains__('project_name'):
                if ProjectForBase.objects.filter(project_name=data['project_name'], parent_id=int(data['parent_id'])).exclude(id=int(data['project_id'])):
                    logger.error("新增项目配置失败: {}".format(BaseEnumeration.CREATE_PROJECT_DATA_ERROR.value))
                    return ReturnJson.faile(BaseEnumeration.CREATE_PROJECT_DATA_ERROR.value)
                pro_info.project_name = data['project_name']
            if data.__contains__('project_type'):
                pro_info.project_type = data['project_type']
            if data.__contains__('project_code'):
                pro_info.project_code = data['project_code']
            if data.__contains__('description'):
                pro_info.description = data['description']
            if data.__contains__('parent_id'):
                pro_info.parent_id = int(data['parent_id'])
            if data.__contains__('abandon_flag'):
                pro_info.abandon_flag = int(data['abandon_flag'])

            pro_info.updated_by_id = user_id
            pro_info.save()
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(BaseEnumeration.UPDATE_PROJECT_ERROR.value)
        else:
            logger.info('更新项目配置成功')
            return ReturnJson.success('更新成功')

    def get(self, request):
        """
        项目配置列表，列表和搜索
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("项目配置列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = ProjectForBase.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = ProjectListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                # roles = ProjectForBase.objects.get_queryset().order_by('-id').filter(abandon_flag=1)
                roles = ProjectForBase.objects.get_queryset().order_by('-abandon_flag', '-id').filter(abandon_flag=1)
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = ProjectListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(BaseEnumeration.SYS_PARAM_ID_ERROR.value)


class VersionApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 版本号相关接口
    """

    def get(self, request):
        """
        项目的版本号配置，列表和搜索
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("系统参数配置列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = VersionForProject.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = VersionForProjectListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                # roles = VersionForProject.objects.get_queryset().order_by('-id')
                roles = VersionForProject.objects.get_queryset().order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = VersionForProjectListSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(BaseEnumeration.SYS_PARAM_ID_ERROR.value)

    def post(self, request):
        """
        新增项目的版本号配置
        :param request:
        :return:
        """
        logger.info('开始执行新增项目的版本号配置接口')
        data = request.data
        user_id = request.user.id
        logger.info("新增数据：{}".format(data))
        try:
            # data = eval(data)
            context = {
                'created_by_id': user_id,
                'updated_by_id': user_id,
                'pro_id': int(data['pro_id']),
            }
            if VersionForProject.objects.filter(type=data['type'], pro_id=int(data['pro_id'])):
                logger.error("新增项目版本号配置失败: {}".format(BaseEnumeration.CREATE_SYS_VERSION_REPEAT_ERROR.value))
                return ReturnJson.faile(BaseEnumeration.CREATE_SYS_VERSION_REPEAT_ERROR.value)
            new_ver = VersionForProjectSerializer(data=data, context=context)
            new_ver.is_valid(raise_exception=True)
            new_ver.save()
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(BaseEnumeration.CREATE_SYS_VERSION_ERROR.value)
        else:
            logger.info('新增项目的版本号配置成功')
            return ReturnJson.success('新增成功')

    def put(self, request):
        """
        更改项目的版本号配置
        :param request:
        :return:
        """
        logger.info('开始执行更新项目的版本号配置接口')
        data = request.data
        user_id = request.user.id
        logger.info("更新数据：{}".format(data))
        try:
            if not data.__contains__('id') or data['id'] == '':
                return ReturnJson.faile(BaseEnumeration.SYS_PARAM_ID_ERROR.value)
            info = VersionForProject.objects.get(id=int(data['id']))
            if data.__contains__('info'):
                if VersionForProject.objects.filter(type=data['info'], pro_id=int(data['pro_id'])).exclude(id=int(data['id'])):
                    logger.error("更新项目版本号配置失败: {}".format(BaseEnumeration.CREATE_SYS_VERSION_REPEAT_ERROR.value))
                    return ReturnJson.faile(BaseEnumeration.CREATE_SYS_VERSION_REPEAT_ERROR.value)
                info.type = data['info']
            if data.__contains__('description'):
                info.description = data['description']
            if data.__contains__('abandon_flag'):
                info.abandon_flag = data['abandon_flag']
            if data.__contains__('pro_id'):
                info.pro_id = data['pro_id']
            info.updated_by_id = user_id
            info.save()
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(BaseEnumeration.UPDATE_SYS_VERSION_ERROR.value)
        else:
            logger.info('更新项目的版本号配置成功')
            return ReturnJson.success('更新项目版本号配置成功')
