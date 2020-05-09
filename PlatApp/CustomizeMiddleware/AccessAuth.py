import re

from django.shortcuts import redirect, HttpResponse
from django.conf import settings


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 1. 获取当前请求的URL
        # request.path_info
        # 2. 获取Session中保存当前用户的权限
        # request.session.get("permission_url_list')
        current_url = request.path_info

        # print(current_url)
        # print("----------------------------------")

        # 根目录路径处理
        if current_url == '/':
            if request.user:
                return redirect('/basecenter/workbench/index/')
            else:
                return redirect('/login/')

        # 当前请求不需要执行权限验证(白名单)
        for url in settings.VALID_URL:
            if re.match(url, current_url):
                return None

        permission_list = request.session.get("permission_list")
        if not permission_list:
            return redirect('/login/')

        flag = False

        for db_url in permission_list:

            # print(db_url)

            if 'api' in current_url:

                if db_url.split('/')[1] in current_url:
                    flag = True
                    break
            else:

                if current_url.split('/')[2] == "subjob":
                    contrast_str = "job"
                else:
                    contrast_str = current_url.split('/')[2]

                # print(current_url.split('/'))
                # print(db_url.split('/'))

                if contrast_str == db_url.split('/')[2]:
                    flag = True
                    break

            # print("----------------------------------")

            # regax = "^{0}*$".format(db_url[:-6])
            # if re.match(regax, current_url[:-6]):
            #     flag = True
            #     break

        if not flag:
            return HttpResponse('无权访问')
