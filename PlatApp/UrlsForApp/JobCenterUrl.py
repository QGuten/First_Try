# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :
from django.urls import path

from PlatApp.PageForApp import JobCenterPages
from PlatApp.RestFulForApp import JobCenterRestFul


app_name = "JobCenter"

urlpatterns = [
    # 页面相关路由配置
    path('job/index/', JobCenterPages.JobIndex.as_view(), name='JobIndex'),
    path('job/create/', JobCenterPages.CreateJobIndex.as_view(), name='CreateJobIndex'),
    path('job/info/', JobCenterPages.JobInfo.as_view(), name='JobInfo'),

    path('subjob/index/', JobCenterPages.SubJobIndex.as_view(), name='SubJobIndex'),
    path('subjob/info/', JobCenterPages.SubJobInfo.as_view(), name='SubJobInfo'),

    path('iteration/index/', JobCenterPages.IterationIndex.as_view(), name='IterationIndex'),
    path('iteration/info/', JobCenterPages.IterationInfo.as_view(), name='IterationInfo'),
    path('iteration/create/', JobCenterPages.CreateIterationIndex.as_view(), name='CreateIterationIndex'),

    path('report/index/', JobCenterPages.ReportIndex.as_view(), name='ReportIndex'),
    path('report/info/', JobCenterPages.ReportInfo.as_view(), name='ReportInfo'),

    # 接口相关路由配置
    path('api/jobs/', JobCenterRestFul.JobApi.as_view(), name='JobApi'),
    path('api/subjobs/', JobCenterRestFul.SubJobApi.as_view(), name='SubJobApi'),
    path('api/reports/', JobCenterRestFul.ReportApi.as_view(), name='ReportApi'),
    path('api/iterations/', JobCenterRestFul.IterationApi.as_view(), name='IterationApi'),
    path('api/iterationrecords/', JobCenterRestFul.IterationRecordApi.as_view(), name='IterationRecordApi'),

    path('api/subjobdata/', JobCenterRestFul.SubJobDataInfoApi.as_view(), name='SubJobDataInfoApi'),
    path('api/reportdata/', JobCenterRestFul.ReportDataInfoApi.as_view(), name='ReportDataInfoApi'),

    path('api/exejob/', JobCenterRestFul.ExeJob.as_view(), name='ExeJob'),
    path('api/exeit/', JobCenterRestFul.ExeIterations.as_view(), name='ExeIterations'),
]
