from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect

import logging
import re

logger = logging.getLogger('AutoApp.app')


def UserPagePeimission(request, login_url=None):

    def check_perms():
        # 检验权限
        permission_list = request.session.get('permission_list')
        for reg in permission_list:
            reg = '^%s$' % reg
            ret = re.search(reg, request.path)
            if ret:
                return True
        return HttpResponseRedirect(login_url)

    return check_perms
