import logging

from django.forms import model_to_dict
from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from PlatApp.models import JobInfoForJobCenter, JobDataForJobCenter, IterationForJobCenter, JobReportListForJobCenter, \
    BaseSysParam, ProjectForBase, ConfigForResources, SubJobDataForJobCenter, SubJobInfoForJobCenter, JobReportInfoForJobCenter, VersionForProject

logger = logging.getLogger('AutoApp.app')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class JobIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试任务列表页面
    """

    template_name = "JobCenter/JobIndex.html"

    def get_context_data(self, **kwargs):
        pro_list = self.request.session['pro_list']
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateJobIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试任务创建页
    """

    template_name = 'JobCenter/CreateJob.html'

    def get_context_data(self, **kwargs):
        """
        重写方法，获取创建页需要展示、配置的数据
        :param kwargs:
        :return:
        """
        pro_list = self.request.session['pro_list']
        # 获取任务类型
        job_type = BaseSysParam.objects.filter(param_key='JobType', abandon_flag=1)
        # 获取夫级为空的项目列表（一级项目列表）
        pro_list = ProjectForBase.objects.filter(parent__isnull=True, abandon_flag=1, id__in=pro_list)
        # 获取接口请求域名列表
        domain_name_list = ConfigForResources.objects.filter(key='DomainName', abandon_flag=1)
        # 获取签名配置列表
        autograph_config_list = ConfigForResources.objects.filter(key='AutographConfig', abandon_flag=1)
        logger.info("获取详情成功")
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class JobInfo(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试任务详情页
    """

    template_name = 'JobCenter/JobInfo.html'

    def get_context_data(self, **kwargs):
        # 获取请求数据中的任务ID
        job_id = self.request.GET.get('id')
        job_info = JobInfoForJobCenter.objects.get(id=job_id)
        setup_info = JobDataForJobCenter.objects.filter(job_id=job_id, if_setup=1)
        case_info = JobDataForJobCenter.objects.filter(job_id=job_id, if_setup=0)
        # 获取签名配置列表
        autograph_config_list = ConfigForResources.objects.filter(key='AutographConfig', abandon_flag=1)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SubJobIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试子任务列表页面
    """

    template_name = "JobCenter/SubJobIndex.html"

    def get_context_data(self, **kwargs):
        job_id = self.request.GET.get('id')
        pro_list = self.request.session['pro_list']
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SubJobInfo(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 测试子任务详情页
    """

    template_name = 'JobCenter/SubJobInfo.html'

    def get_context_data(self, **kwargs):
        # 获取请求数据中的任务ID
        job_id = self.request.GET.get('id')
        job_info = SubJobInfoForJobCenter.objects.get(id=job_id)
        setup_info = SubJobDataForJobCenter.objects.filter(job_id=job_id, if_setup=1)
        case_info = SubJobDataForJobCenter.objects.filter(job_id=job_id, if_setup=0)
        # 获取签名配置列表
        autograph_config_list = ConfigForResources.objects.filter(key='AutographConfig', abandon_flag=1)
        return locals()


# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class IterationIndex(ListView):
#     """
#     @Author: 朱孟彤
#     @desc: 迭代列表页
#     """
#
#     template_name = "JobCenter/IterationIndex.html"
#     model = IterationForJobCenter
#     context_object_name = "iteration_list"
#     paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class IterationIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 迭代列表页
    """

    template_name = "JobCenter/IterationIndex.html"

    def get_context_data(self, **kwargs):
        pro_list = self.request.session['pro_list']
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class IterationInfo(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 迭代详情页
    """

    template_name = "JobCenter/IterationInfo.html"

    def get_context_data(self, **kwargs):
        # 获取请求数据中的任务ID
        it_id = self.request.GET.get('id')
        data_info = IterationForJobCenter.objects.get(id=int(it_id))

        jobs = [model_to_dict(i) for i in data_info.job.all()]

        pro_list = self.request.session['pro_list']
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CreateIterationIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 创建迭代页
    """

    template_name = "JobCenter/CreateIterations.html"

    def get_context_data(self, **kwargs):
        pro_list = self.request.session['pro_list']
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1, id__in=pro_list)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReportIndex(ListView):
    """
    @Author: 朱孟彤
    @desc: 报告管理列表页
    """

    template_name = "JobCenter/ReportIndex.html"
    model = JobReportListForJobCenter
    context_object_name = "report_list"
    paginate_by = 10


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReportInfo(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 报告详情页
    """

    template_name = "JobCenter/ReportInfo.html"

    def get_context_data(self, **kwargs):
        # 获取请求数据中的任务ID
        report_id = self.request.GET.get('id')
        report_info = JobReportListForJobCenter.objects.get(id=int(report_id))
        case_info = JobReportInfoForJobCenter.objects.filter(step_id__isnull=True, report_id=int(report_id))
        return locals()
