from PlatApp.models import CaseInfoForCaseCenter, CaseSuiteForCaseCenter

from django_filters import rest_framework as filters


class CaseInfoFilter(filters.FilterSet):
    """
    @Author: 朱孟彤
    @desc: 查询用例信息用
    """
    class Meta:
        model = CaseInfoForCaseCenter
        fields = ['id', 'pro', 'case_name', 'case_name', 'case_type']


class CaseSuiteFilter(filters.FilterSet):
    """
    @Author: 朱孟彤
    @desc: 查询用例套件用
    """
    class Meta:
        model = CaseSuiteForCaseCenter
        fields = ['id', 'pro', 'suite_name', 'case_type']

