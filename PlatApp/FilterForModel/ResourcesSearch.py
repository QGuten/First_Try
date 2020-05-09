from PlatApp.models import RequestsForResources

from django_filters import rest_framework as filters


class RequestsInfoFilter(filters.FilterSet):
    """
    @Author: 朱孟彤
    @desc: 查询接口信息
    """
    class Meta:
        model = RequestsForResources
        fields = ['id', 'pro', 'case_name', 'case_name', 'case_type']


