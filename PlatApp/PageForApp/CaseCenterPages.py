# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :
import logging

from django.forms import model_to_dict
from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from PlatApp.models import CaseInfoForCaseCenter, CaseSuiteForCaseCenter, ProjectForBase, BaseSysParam

logger = logging.getLogger('AutoApp.app')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CaseIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试用例列表页面
    """

    template_name = "CaseCenter/CaseIndex.html"

    def get_context_data(self, **kwargs):
        pro_list = self.request.session['pro_list']
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateCaseIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 创建测试用例页面
    """

    template_name = "CaseCenter/CreateCase.html"

    def get_context_data(self, **kwargs):
        pro_list = self.request.session['pro_list']
        # 获取系统配置表 参数类型配置
        params_list = BaseSysParam.objects.filter(param_key='ParamsType', abandon_flag=1)
        params_type_list = [i.param_value for i in params_list]
        # 获取测试用例类型
        case_type = BaseSysParam.objects.filter(param_key='CaseType', abandon_flag=1)
        # 获取夫级为空的项目列表（一级项目列表）
        pro_list = ProjectForBase.objects.filter(parent__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CaseInfo(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试用例详情页
    """

    template_name = "CaseCenter/CaseInfo.html"

    def get_context_data(self, **kwargs):
        """
        重写方法，获取测试用例详情页展示内容
        :param kwargs:
        :return:
        """
        # 获取请求数据中的用例id
        re_id = self.request.GET.get('id')
        # 获取系统配置表 参数类型配置
        params_list = BaseSysParam.objects.filter(param_key='ParamsType', abandon_flag=1)
        params_type_list = [i.param_value for i in params_list]
        # 根据用例id获取用例数据
        case_info = CaseInfoForCaseCenter.objects.get(id=re_id)
        # 获取用例关联的用例步骤
        a = case_info.step_list.all()
        # 测试用例步骤的数据类型转换 queryset -> dict
        step_list = [model_to_dict(i) for i in a]
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SuiteIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试套件列表页面
    """

    template_name = "CaseCenter/SuiteIndex.html"

    def get_context_data(self, **kwargs):
        pro_list = self.request.session['pro_list']
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SuiteInfo(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试套件详情页
    """

    template_name = "CaseCenter/SuiteInfo.html"

    def get_context_data(self, **kwargs):
        """
        重写方法，获取测试套件详情展示内容
        :param kwargs:
        :return:
        """
        # 获取请求数据中的套件id
        re_id = self.request.GET.get('id')
        # 获取测试套件的详细信息
        suite_info = CaseSuiteForCaseCenter.objects.get(id=re_id)
        # 根据测试套件ID，获取测试用例列表
        case_list = CaseInfoForCaseCenter.objects.filter(case_suite=re_id)
        # 拼接套件中的测试用例与操作步骤的数据集合
        step_all = []
        for case in case_list:
            step_dict = {}
            step_dict.update(model_to_dict(case))
            a = case.step_list.all()
            step_list = [model_to_dict(i) for i in a]
            step_dict['step_list'] = step_list
            step_all.append(step_dict)
        return locals()
