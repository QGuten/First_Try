# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @desc    :
from django.urls import path

from PlatApp.PageForApp import ResourcesPages
from PlatApp.RestFulForApp import ResourcesRestFul


app_name = "ResourceCenter"

urlpatterns = [
    # 页面相关配置
    path('requests/index/', ResourcesPages.RequestsIndex.as_view(), name='RequestsIndex'),
    path('requests/info/', ResourcesPages.RequestsInfo.as_view(), name='RequestsInfo'),
    path('requests/create/', ResourcesPages.CreateRequestsIndex.as_view(), name='CreateRequestsIndex'),
    path('configs/index/', ResourcesPages.ConfigIndex.as_view(), name='ConfigIndex'),
    # path('sqls/index/', ResourcesPages.SQLIndex.as_view(), name='SQLIndex'),

    # 接口相关配置
    path('api/requests/', ResourcesRestFul.RequestsApi.as_view(), name='RequestsApi'),
    path('api/configs/', ResourcesRestFul.ConfigApi.as_view(), name='ConfigApi'),

    path('api/getrequestsdocsforurl/', ResourcesRestFul.GetRequestsDocsForUrl.as_view(), name='GetRequestsDocsForUrl'),
    path('api/requeststocase/', ResourcesRestFul.RequestsToCase.as_view(), name='RequestsToCase'),
]
