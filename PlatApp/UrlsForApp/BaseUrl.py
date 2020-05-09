# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @desc    :
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from PlatApp.PageForApp import BasePages
from PlatApp.RestFulForApp import BaseRestFul


app_name = "BaseCenter"

urlpatterns = [
    # 页面配置
    path('config/index/', BasePages.SystemConfigIndex.as_view(), name='SysConfig'),
    path('sysjob/index/', BasePages.SystemJobIndex.as_view(), name='SysJob'),
    path('workbench/index/', BasePages.WorkbenchIndex.as_view(), name='WorkbenchIndex'),
    path('sysproject/index/', BasePages.ProjectForBaseIndex.as_view(), name='SysProject'),
    path('sysjob/record/', BasePages.ReDocsJobRecord.as_view(), name='ReDocsJobRecord'),

    # 接口配置

    path('api/sysparam/', BaseRestFul.SysParamApi.as_view(), name='SysParamApi'),

    path('api/project/', BaseRestFul.ProjectApi.as_view(), name='ProjectApi'),

    path('api/version/', BaseRestFul.VersionApi.as_view(), name='ProjectVersionApi'),

    # wiki配置
    # path('WikiDocsIndex/', BasePages.WikiDocsIndex, name='WikiDocsIndex'),
    # path('CreateWikiDocs/', BasePages.CreateWikiDocs, name='CreateWikiDocs'),
    # path('WikiDocsInfo/', BasePages.WikiDocsInfo, name='WikiDocsInfo'),
    # # path('WikiDocs/', BaseRestFul.WikiDocs.as_view(), name='WikiDocs'),
    # path('WikiDocs/', BaseRestFul.WikiDocs, name='WikiDocs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
