# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @desc    :
import logging

from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from PlatApp.models import RequestsForResources, ConfigForResources, ProjectForBase, BaseSysParam


logger = logging.getLogger('AutoApp.app')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RequestsIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 接口管理列表页
    """

    template_name = "ResourcesCenter/RequestsIndex.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        pro_list = self.request.session['pro_list']
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RequestsInfo(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 接口管理，接口详情页
    """

    template_name = "ResourcesCenter/RequestInfo.html"

    def get_context_data(self, **kwargs):
        """
        重写方法，获取需展示的详情数据
        :param kwargs:
        :return:
        """
        # 获取接口ID
        re_id = self.request.GET.get('id')
        pro_list = self.request.session['pro_list']
        # 根据接口ID，获取接口详情地址
        re_info = RequestsForResources.objects.get(id=re_id)
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        # 获取系统配置表 请求方式配置
        method_list = BaseSysParam.objects.filter(param_key='MethodType', abandon_flag=1)
        # 获取系统配置表 参数类型配置
        # params_type_list = BaseSysParam.objects.values_list('param_value').filter(param_key='ParamsType', abandon_flag=1)
        params_list = BaseSysParam.objects.filter(param_key='ParamsType', abandon_flag=1)
        params_type_list = [i.param_value for i in params_list]
        # 获取测试用例生成规则名称配置
        config_list = BaseSysParam.objects.filter(param_key='CaseReParamsType', abandon_flag=1)
        logger.info("接口详情页数据获取成功")
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateRequestsIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 接口管理，新建接口页
    """

    template_name = "ResourcesCenter/CreateRequests.html"

    def get_context_data(self, **kwargs):
        """
        重写方法，获取需展示的详情数据
        :param kwargs:
        :return:
        """

        re_data = {
            're_name': self.request.GET.get('re_name'),
            'developer': self.request.GET.get('developer'),
            'edition': self.request.GET.get('edition'),
            're_path': self.request.GET.get('re_path'),
            'description': self.request.GET.get('description'),
        }

        p_list = ['re_name', 'developer', 'edition', 're_path', 'description']
        for p in p_list:
            if not re_data[p]:
                re_data[p] = ''

        pro_list = self.request.session['pro_list']
        # 获取测试用例生成规则名称配置
        config_list = BaseSysParam.objects.filter(param_key='CaseReParamsType', abandon_flag=1)
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        # 获取系统配置表 请求方式配置
        method_list = BaseSysParam.objects.filter(param_key='MethodType', abandon_flag=1)
        # 获取系统配置表 参数类型配置
        params_list = BaseSysParam.objects.filter(param_key='ParamsType', abandon_flag=1)
        # 用例类型配置列表
        case_type_list = BaseSysParam.objects.filter(param_key='CaseReParamsType', abandon_flag=1)
        logger.info("新建接口页数据获取成功")
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 配置管理列表页
    """

    template_name = "ResourcesCenter/ConfigIndex.html"

    def get_context_data(self, **kwargs):
        """
        重写方法，获取配置管理列表页，需要关联的配置信息
        :param kwargs:
        :return:
        """
        pro_list = self.request.session['pro_list']
        # 获取项目列表
        project_list = ProjectForBase.objects.filter(abandon_flag=1, parent__id__isnull=True, id__in=pro_list)
        logger.info("配置管理列表页数据获取成功")
        return locals()


# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class SQLIndex(TemplateView):
#     """
#     @Author: 朱孟彤
#     @desc: SQL管理列表页
#     """
#
#     template_name = "ResourcesCenter/SQLIndex.html"
