# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : 
# @desc    :
from PlatApp.SerializerType.ManyKeyType import ManyKeyForTitle, ManyKeyForName
from PlatApp.models import OpsUser, Menu, Role  # , Permission

from rest_framework import serializers


class OpsUserSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 用户信息列表序列化
    """
    name = serializers.SerializerMethodField()
    role = ManyKeyForTitle()
    pro = ManyKeyForName()

    class Meta:
        model = OpsUser
        fields = ('id', 'last_name', 'first_name', 'username', 'email', 'mobile_no', 'department', 'name', 'role', 'pro', 'is_active')

    def get_name(self, obj):

        return obj.last_name+obj.first_name


class MenuSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 菜单序列化（新增）
    """
    icon = serializers.CharField(allow_blank=True)

    class Meta:
        model = Menu
        fields = ('id', 'title', 'icon', 'url', 'order', 'abandon_flag')


class MenuReSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 菜单序列化（查询）
    """
    parent = serializers.CharField(source='parent.title', allow_null=True)

    class Meta:
        model = Menu
        fields = ('id', 'title', 'parent', 'icon', 'url', 'order', 'abandon_flag')


# class PermissionAddSerializer(serializers.ModelSerializer):
#     """
#     @Author: 朱孟彤
#     @desc: 权限序列化（查询）
#     """
#
#     class Meta:
#         model = Permission
#         fields = ('id', 'title', 'url', 'menu_id', 'order', 'abandon_flag')
#
#
# class PermissionSerializer(serializers.ModelSerializer):
#     """
#     @Author: 朱孟彤
#     @desc: 权限序列化（查询）
#     """
#     menu_title = serializers.ReadOnlyField()
#
#     class Meta:
#         model = Permission
#         fields = ('id', 'title', 'url', 'menu', 'order', 'menu_title', 'abandon_flag')


class RoleSerializer(serializers.ModelSerializer):
    """
    @Author: 朱孟彤
    @desc: 角色序列化（查询）
    """
    # permissions = serializers.StringRelatedField(many=True, read_only=True)
    permissions = ManyKeyForTitle()

    class Meta:
        model = Role
        fields = ('id', 'title', 'permissions', 'abandon_flag')
