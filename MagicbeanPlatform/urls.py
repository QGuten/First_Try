"""MagicbeanPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from PlatApp import views
from PlatApp.PageForApp import UsersPages

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.test_temp, name='test_temp'),

    path('mdeditor/', include('mdeditor.urls')),

    # 用户权限相关接口和页面
    path('login/', UsersPages.LoginIndex.as_view(), name='login'),
    path('usercenter/', include('PlatApp.UrlsForApp.UsersUrl', namespace='UserCenter')),

    # 系统级相关页面和接口
    path('basecenter/', include('PlatApp.UrlsForApp.BaseUrl', namespace='BaseCenter')),

    # 资源库的相关页面和接口
    path('resourcecenter/', include('PlatApp.UrlsForApp.ResourcesUrl', namespace='ResourceCenter')),

    # 用例库的相关页面和接口
    path('casecenter/', include('PlatApp.UrlsForApp.CaseCenterUrl', namespace='CaseCenter')),

    # 任务库的相关页面和接口
    path('jobcenter/', include('PlatApp.UrlsForApp.JobCenterUrl', namespace='JobCenter')),
]
