from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class GoodsPagination(PageNumberPagination):
    """
    @Author: 朱孟彤
    @desc: 自定义分页配置
    """
    page_size = 10  # 默认分页
    page_size_query_param = 'limit'  # 自定义分页数量
    page_query_param = 'page'  # 指定分页参数为p
    max_page_size = 100  # 单页最大数量

    def get_paginated_response(self, data):
        """
        重写方法，设定返回值格式
        :param data: 返回数据
        :return: 根据设定的返回response对象
        """
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('code', 200),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
