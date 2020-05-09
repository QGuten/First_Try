# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @desc    :
import logging
import markdown
from django.db.models import Count

from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import render

from PlatApp.FormsForApp.MDEditorForm import MDEditorModleForm
from PlatApp.models import BaseSysParam, ProjectForBase, JobForBase, ConfigForResources, JobRecordForBase, MDEditorForm, SubJobInfoForJobCenter
from PlatApp.models import RequestsForResources, CaseInfoForCaseCenter, IterationForJobCenter

logger = logging.getLogger('AutoApp.app')


def WikiDocsIndex(request):
    """
    文档首页
    :param request:
    :return:
    """
    docs = MDEditorForm.objects.all()
    return render(request, 'BaseCenter/WikiIndex.html', locals())


def CreateWikiDocs(request):
    """
    创建文档
    :param request:
    :return:
    """
    # if request.method == 'GET':
    form = MDEditorModleForm()
    return render(request, 'BaseCenter/CreateWiki.html', locals())


def WikiDocsInfo(request):
    """
    文档详情
    :param request:
    :return:
    """
    if request.method == 'GET':
        docs_id = request.GET.get('id')
        docs_info = MDEditorForm.objects.get(id=int(docs_id))
        # docs_info.context = markdown.markdown(docs_info.context, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.toc', ])
        return render(request, 'BaseCenter/WikiInfo.html', locals())
        # return render(request, 'testPage.html', locals())
    else:
        return render(request, 'BaseCenter/WikiInfo.html', locals())


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProjectForBaseIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 项目配置页面
    """

    template_name = "BaseCenter/SystemProject.html"

    def get_context_data(self, **kwargs):
        project_list = ProjectForBase.objects.filter(abandon_flag=1)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SystemConfigIndex(ListView):
    """
    @Author: 朱孟彤
    @desc: 系统配置页
    """

    template_name = "BaseCenter/SystemConfig.html"
    model = BaseSysParam
    context_object_name = 'sys_params'
    paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SystemJobIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 系统任务页
    """

    template_name = "BaseCenter/SystemJob.html"

    def get_context_data(self, **kwargs):
        # 任务列表
        job_list = JobForBase.objects.all()
        # 接口文档地址配置列表
        config_list = ConfigForResources.objects.filter(key="RequestDocsPath", abandon_flag=1)
        # 用例类型配置列表
        case_type_list = BaseSysParam.objects.filter(param_key='CaseReParamsType', abandon_flag=1)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class WorkbenchIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 我的工作台页
    """

    template_name = "BaseCenter/WorkbenchIndex.html"

    def get_context_data(self, **kwargs):
        pro_list = self.request.session['pro_list']

        it_num = IterationForJobCenter.objects.filter(pro__id__in=pro_list).__len__()
        re_num = RequestsForResources.objects.filter(project__parent__id__in=pro_list).__len__()
        case_num = CaseInfoForCaseCenter.objects.filter(pro__parent__id__in=pro_list).__len__()
        job_nub = SubJobInfoForJobCenter.objects.filter(pro__id__in=pro_list).__len__()
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReDocsJobRecord(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 接口文档解析任务详情
    """

    template_name = "BaseCenter/SystemJobRecord.html"

    def get_context_data(self, **kwargs):
        # 获取任务信息
        job_info = JobForBase.objects.get(id=1)
        # 获取任务执行记录
        job_record = JobRecordForBase.objects.filter(job_id=1).order_by('created_at')
        return locals()
