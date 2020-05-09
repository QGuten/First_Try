#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re

from django.forms import model_to_dict
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.db.models import Q
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from django_filters import rest_framework

from rest_framework import mixins, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from common.ReturnJson import ReturnJson

from MagicbeanPlatform.settings import REGEX_MOBILE, REGEX_EMAIL

from PlatApp.CustomizeMiddleware.SetSession import initial_session
from PlatApp.RestFulForApp.PageRestFul import GoodsPagination
from PlatApp.CustomizeEnumeration.UserEnumeration import *
from PlatApp.models import OpsUser, Menu, Role  # , Permission
from PlatApp.FilterForModel.UsersSearch import UserFilter
from PlatApp.SerializersForModel.UsersSerializer import OpsUserSerializer, MenuSerializer, \
    RoleSerializer, MenuReSerializer  # PermissionSerializer, PermissionAddSerializer

logger = logging.getLogger('AutoApp.app')


@method_decorator(csrf_exempt, name='dispatch')
class SingIn(View):
    """
    @Author: 朱孟彤
    @desc: 登录接口
    """

    def post(self, request):
        """
        登录接口
        :param request:
        :return:
        """
        logger.info('进入登录接口 --- 开始校验请求参数')
        data = request.POST.dict()
        logger.info(str(data))
        if not data.__contains__('info') or not data.__contains__('pwd'):
            # return JsonResponse({'status': 201, 'msg': '用户名/密码为空，请重新输入'})
            error_msg = "用户名/密码为空，请重新输入"
            logger.error('用户名/密码为空，请重新输入')
            return ReturnJson.faile(error_msg)
            # return render(request, 'login.html', locals())
        logger.info('判断用户是否存在')
        try:
            info = OpsUser.objects.values('id', 'username').filter(
                Q(mobile_no=data['info']) | Q(email=data['info']) | Q(username=data['info']))
            if bool(info):
                logger.info('用户存在开始登录')
                username = info[0]['username']
                user = auth.authenticate(username=username, password=data['pwd'])
                if user:
                    if user.is_active:
                        logger.info('开始登录')
                        auth.login(request, user)
                        logger.info('登录成功，开始添加权限')
                        logger.info(info[0])
                        request.session['user_id'] = info[0]['id']  # 用户id注入session
                        # 将权限列表和权限菜单列表注入session
                        initial_session(info[0]['id'], request)
                        # initial_session(user, request)
                        logger.info('添加页面权限菜单')
                        return ReturnJson.success('登录成功')
                        # return HttpResponseRedirect('/BaseCenter/WorkbenchIndex/')
                    else:
                        error_msg = "该用户已被禁，请联系管理员"
                        logger.error('该用户已被禁，请联系管理员')
                        return ReturnJson.faile(error_msg)
                        # return render(request, 'login.html', locals())
                else:
                    error_msg = "用户名密码错误，请重新输入"
                    logger.error('用户名密码错误，请重新输入')
                    # error_msg = "请重新核对您的用户名和密码"
                    # logger.error('user为空')
                    return ReturnJson.faile(error_msg)
                    # return render(request, 'login.html', locals())
        except Exception as ex:
            error_msg = "系统异常，请稍后再试"
            logger.error(ex)
            return ReturnJson.faile(error_msg)
            # return render(request, 'login.html', locals())


class SetPassword(APIView):
    """
    @Author: 朱孟彤
    @desc: 设置密码接口
    """

    def post(self, request):
        """
        post方法，设置登录密码
        :return:
        """
        logger.info('设置登录密码接口')
        data = request.data
        logger.info("开始修改密码")
        password1 = data.get('password_1')
        password2 = data.get('password_2')
        logger.info("修改的用户ID为: {}".format(data['user_id']))
        if password1 != password2:
            logger.error('密码不一致，请重新输入')
            return ReturnJson.faile(UserEnumeration.PASSWORD_INPUT_ERROR.value)
        else:
            user_info = OpsUser.objects.get(id=int(data['user_id']))
            logger.info("获取到的用户信息为: {}".format(user_info))
            try:
                user_info.set_password(password2)
                logger.info("修改密码中")
                user_info.save()
                logger.info("修改密码成功")
                return ReturnJson.success("重置密码成功")
            except Exception as e:
                logger.error('修改密码失败:{}'.format(e))
                return ReturnJson.faile(UserEnumeration.SET_PASSWORD_ERROR.value)


# @method_decorator(csrf_exempt, name='dispatch')
class SignOut(View):
    """
    @Author: 朱孟彤
    @desc: 退出登录接口
    """

    def post(self, request):
        """
        post 退出登录接口
        :param request:
        :return:
        """
        user_id = request.user.id
        logger.info("用户" + str(user_id) + "退出登录")
        try:
            auth.logout(request)
            request.session.clear()
            # return HttpResponseRedirect('/login/', locals())
            return ReturnJson.success('退出成功')
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(UserEnumeration.SIGNOUT_ERROR.value)


# class GetUserList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     """
#     @Author: 朱孟彤
#     @desc: 获取用户列表
#     """
#
#     queryset = OpsUser.objects.all()
#     filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
#     filter_class = UserFilter
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     serializer_class = OpsUserSerializer
#     paginate_by = 10
#
#     def list(self, request, *args, **kwargs):
#         """
#         根据格式返回指定的数据
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         count = len(serializer.data)
#         return Response({"code": 0, "data": serializer.data, "count": count})


class UsersApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 用户相关Api
    """

    @transaction.atomic
    def post(self, request):
        """
        post方法 新增用户
        :param request:
        :return:
        """
        logger.info('开始执行新增用户接口')
        data = request.data
        logger.info('开始进行参数校验')
        logger.info(str(data))
        if not data.__contains__('username') or data['username'] == '':
            return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        if not data.__contains__('password') or data['password'] == '':
            return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        if not data.__contains__('last_name') or data['last_name'] == '':
            return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        if not data.__contains__('first_name') or data['first_name'] == '':
            return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        if not data.__contains__('department') or data['department'] == '':
            return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        if not data.__contains__('roles') or len(data['roles']) == '0':
            return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        logger.info('参数校验通过')
        # 开始检测用户是否已注册
        # 条件1：用户名不可重复
        if OpsUser.objects.filter(username=data['username']):
            return ReturnJson.faile(UserEnumeration.REGISTER_USERNAME_FORGET_ERROR.value)
        sid = transaction.savepoint()
        try:
            logger.info('用户不存在，开始创建新用户')
            user_info = OpsUser.objects.create_user(username=data['username'], password=data['password'])
            user_info.last_name = data['last_name']
            user_info.first_name = data['first_name']
            user_info.mobile_no = data['mobile_no']
            user_info.email = data['email']
            user_info.department = data['department']
            user_info.save()
            logger.info("给用户添加角色")
            for i in data['roles']:
                user_info.role.add(i)
            logger.info("给用户添加角色成功")
        except Exception as ex:
            logger.error(ex)
            transaction.rollback(sid)
            return ReturnJson.faile(UserEnumeration.REGISTER_ERROR.value)
        else:
            transaction.savepoint_commit(sid)
            return ReturnJson.success('新增成功')

    @transaction.atomic
    def put(self, request):
        """
        post方法，更新用户信息
        :param request:
        :return:
        """
        logger.info('开始执行更新用户信息接口')
        data = request.data
        logger.info('开始进行参数校验：{}'.format(data))
        if not data.__contains__('user_id') or data['user_id'] == '':
            return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        # 开始检测用户是否已注册
        # 条件1：用户名不可重复
        # a = OpsUser.objects.filter(username=data['username']).exclude(id=data['user_id'])
        logger.info('参数校验通过')
        sid = transaction.savepoint()
        try:
            logger.info('开始更新用户信息')
            user = OpsUser.objects.get(id=data['user_id'])
            if data.__contains__('username'):
                if OpsUser.objects.filter(username=data['username']).exclude(id=data['user_id']):
                    return ReturnJson.faile(UserEnumeration.REGISTER_USERNAME_FORGET_ERROR.value)
                else:
                    user.username = data['username']
            if data.__contains__('last_name'):
                user.last_name = data['last_name']
            if data.__contains__('first_name'):
                user.first_name = data['first_name']
            if data.__contains__('department'):
                user.department = data['department']
            if data.__contains__('mobile_no'):
                user.mobile_no = data['mobile_no']
            if data.__contains__('email'):
                user.email = data['email']
            if data.__contains__('abandon_flag'):
                user.is_active = int(data['abandon_flag'])
            # 更改角色和项目
            if data.__contains__('roles'):
                roles = [int(r) for r in data['roles']]
                user.role.clear()
                user.role.add(*roles)
            if data.__contains__('pros'):
                pros = [int(r) for r in data['pros']]
                user.pro.clear()
                user.pro.add(*pros)

            user.save()
            logger.info('更新用户信息成功')
            transaction.savepoint_commit(sid)
            return ReturnJson.success("更新用户信息成功")
        except Exception as e:
            logger.error('更新用户信息失败：{}'.format(e))
            transaction.rollback(sid)
            return ReturnJson.faile(UserEnumeration.UPDATE_USER_INFO_ERROR.value)

    def get(self, request):
        """
        获取用户列表
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("获取用户列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = OpsUser.objects.filter(**search_data).order_by('-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = OpsUserSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = OpsUser.objects.get_queryset().order_by('-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = OpsUserSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(UserEnumeration.GET_INFO_ERROR.value)


class MenuApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 菜单相关操作
    """

    @transaction.atomic
    def post(self, request):
        """
        post方法 新增菜单
        :param request:
        :return:
        """
        logger.info('开始执行新增菜单接口')
        data = request.data
        logger.info('开始进行参数校验')
        logger.info(str(data))
        params_list = ['title', 'order', 'url']
        for params in params_list:
            if not data.__contains__(params) or data[params] == '':
                return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        logger.info('参数校验通过')
        sid = transaction.savepoint()
        try:
            add_menu = MenuSerializer(data=data)
            add_menu.is_valid(raise_exception=True)
            new_menu = add_menu.save()
            if data.__contains__('parent_id'):
                info = Menu.objects.get(id=new_menu.id)
                info.parent_id = data['parent_id']
                info.save()
            transaction.savepoint_commit(sid)
        except Exception as ex:
            logger.error(ex)
            transaction.savepoint_rollback(sid)
            return ReturnJson.faile(UserEnumeration.CREATE_MENU_ERROR.value)
        else:
            logger.info('新增菜单成功')
            return ReturnJson.success('新增成功')

    def put(self, request):
        """
        put方法，更新菜单信息
        :param request:
        :return:
        """
        logger.info('开始执行更新菜单信息接口')
        data = request.data
        logger.info('开始更新数据')
        logger.info(str(data))
        try:
            if not data.__contains__('menu_id') or data['menu_id'] == '':
                return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
            menu_info = Menu.objects.filter(id=int(data['menu_id'])).first()
            if data.__contains__('title'):
                menu_info.title = data['title']
            if data.__contains__('icon'):
                menu_info.icon = data['icon']
            if data.__contains__('abandon_flag'):
                menu_info.abandon_flag = data['abandon_flag']
            menu_info.save()
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(UserEnumeration.CREATE_MENU_ERROR.value)
        else:
            logger.info('更新菜单信息成功')
            return ReturnJson.success('更新成功')

    def get(self, request):
        """
        获取菜单列表
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("获取菜单列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = Menu.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = MenuReSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = Menu.objects.get_queryset().order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = MenuReSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(UserEnumeration.GET_INFO_ERROR.value)


# class GetMenuList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     """
#     @Author: 朱孟彤
#     @desc: 获取菜单列表
#     """
#
#     queryset = Menu.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     serializer_class = MenuReSerializer
#
#     def list(self, request, *args, **kwargs):
#         """
#         根据格式返回指定的数据
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         count = len(serializer.data)
#         return Response({"code": 200, "data": serializer.data, "count": count})


# class GetRoleList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     """
#     @Author: 朱孟彤
#     @desc: 获取角色列表
#     """
#
#     queryset = Role.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     serializer_class = RoleSerializer
#
#     def list(self, request, *args, **kwargs):
#         """
#         根据格式返回指定的数据
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         count = len(serializer.data)
#         return Response({"code": 200, "data": serializer.data, "count": count})


class RoleApi(APIView):
    """
    @Author: 朱孟彤
    @desc: 角色相关Api
    """

    def post(self, request):
        """
        post方法 新增角色
        :param request:
        :return:
        """
        logger.info('开始执行新增角色接口')
        data = request.data
        logger.info('开始进行参数校验')
        logger.info(str(data))
        if not data.__contains__('title') or data['title'] == '':
            return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
        logger.info('参数校验通过')
        try:
            new_role = Role()
            new_role.title = data['title']
            new_role.save()
            for i in data['role_list']:
                new_role.permissions.add(i)
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(UserEnumeration.CREATE_MENU_ERROR.value)
        else:
            logger.info('新增角色成功')
            return ReturnJson.success('新增成功')

    def put(self, request):
        """
        put方法，更新角色信息
        :param request:
        :return:
        """
        logger.info('开始执行更新权限菜单信息')
        data = request.data
        logger.info('开始更新数据')
        logger.info(str(data))
        try:
            if not data.__contains__('role_id') or data['role_id'] == '':
                return ReturnJson.faile(UserEnumeration.REGISTER_USER_TYPE_ERROR.value)
            role_info = Role.objects.get(id=int(data['role_id']))
            if data.__contains__('title'):
                role_info.title = data['title']
            if data.__contains__('abandon_flag'):
                role_info.abandon_flag = data['abandon_flag']
            if data.__contains__('per_list'):
                g_per_list = data['per_list']
                role_info.permissions.clear()
                [role_info.permissions.add(menu) for menu in g_per_list]
            role_info.save()
        except Exception as ex:
            logger.error(ex)
            return ReturnJson.faile(UserEnumeration.CREATE_MENU_ERROR.value)
        else:
            logger.info('更新菜单信息成功')
            return ReturnJson.success('更新成功')

    def get(self, request):
        """
        获取角色列表
        :param request:
        :return:
        """
        data = request.GET.get('search_data')
        logger.info("获取角色列表，搜索数据:{}".format(data))
        try:
            if data:
                search_data = {}
                data = eval(data)
                for key, value in data.items():
                    if bool(key) and bool(value):
                        search_data[key] = data[key]
                roles = Role.objects.filter(**search_data).order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页查询数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 对查询数据进行序列化
                roles_ser = RoleSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info

            else:
                # 没有搜索条件和搜索类型，那么默认为显示全部信息
                # 根据id排序，搜索数据
                roles = Role.objects.get_queryset().order_by('-abandon_flag', '-id')
                # 自定义分页实例化
                page = GoodsPagination()
                # 根据分页处理数据
                page_roles = page.paginate_queryset(queryset=roles, request=request, view=self)
                # 查询数据序列化处理
                roles_ser = RoleSerializer(instance=page_roles, many=True)
                # 返回数据，以及前后页的url
                result_info = page.get_paginated_response(roles_ser.data)
                # return Response(roles_ser.data)  # 只返回数据
                return result_info
        except Exception as e:
            logger.error(e)
            return ReturnJson.faile(UserEnumeration.GET_INFO_ERROR.value)
