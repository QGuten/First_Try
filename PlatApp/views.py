from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

import logging

logger = logging.getLogger('AutoApp.app')


@login_required(login_url='/login/')
def test_temp(request):
    """
    平台首页
    :param request:
    :return:
    """
    return redirect('/basecenter/workbench/index/')