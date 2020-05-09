# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    :
# @desc    :
from django.urls import path

from PlatApp.PageForApp import CaseCenterPages
from PlatApp.RestFulForApp import CaseCenterRestFul


app_name = "CaseCenter"

urlpatterns = [
    # 页面相关路由配置
    path('case/index/', CaseCenterPages.CaseIndex.as_view(), name='CaseIndex'),
    path('case/info/', CaseCenterPages.CaseInfo.as_view(), name='CaseInfo'),
    path('case/create/', CaseCenterPages.CreateCaseIndex.as_view(), name='CreateCaseIndex'),

    path('suite/index/', CaseCenterPages.SuiteIndex.as_view(), name='SuiteIndex'),
    path('suite/info/', CaseCenterPages.SuiteInfo.as_view(), name='SuiteInfo'),

    # 接口路由配置
    path('api/caseinfo/', CaseCenterRestFul.CaseInfoApi.as_view(), name='CaseInfoApi'),

    path('api/casesuite/', CaseCenterRestFul.CaseSuiteApi.as_view(), name='CaseSuiteApi'),

]
