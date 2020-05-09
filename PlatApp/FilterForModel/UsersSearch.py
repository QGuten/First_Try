from PlatApp.models import OpsUser

from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    """
    @Author: 朱孟彤
    @desc: 查询用户信息字段配置
    """
    class Meta:
        model = OpsUser
        fields = ['id', 'username', 'mobile_no', 'email']

