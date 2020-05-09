# 将当前登录人的所有权限注入session中
from django.forms import model_to_dict

from PlatApp.models import Role

import logging

logger = logging.getLogger('AutoApp.app')


def initial_session(user_obj, request):
    """
    @Author: 朱孟彤
    @desc: 将当前登录人的所有权限url列表和自己构建的所有菜单权限字典注入session
    :param user_obj: 当前登录用户对象
    :param request: 请求对象HttpRequest
    """
    # 查询当前登录人的所有权限列表
    logger.info('查询当前登录人的所有权限列表')
    ret = Role.objects.filter(opsuser=user_obj).values('permissions__url', 'permissions__title', 'permissions__icon', 'permissions__id', 'permissions__order', 'permissions__parent__title', 'permissions__parent__icon').distinct()
    pro_list = list(Role.objects.filter(opsuser=user_obj).values_list('opsuser__pro__id', flat=True))
    # print(ret)
    permission_list = []
    permission_menu_dict = {}
    logger.info('获取用户权限列表用于中间件中权限校验')
    for item in ret:
        # 获取用户权限列表用于中间件中权限校验
        permission_list.append(item['permissions__url'])
        menu_pk = item['permissions__parent__title']
        if not item['permissions__parent__title']:
            permission_menu_dict[item['permissions__title']] = {
                "title": item['permissions__title'],
                "url": item["permissions__url"],
                "order": item["permissions__order"],
                "icon": item["permissions__icon"],
            }
        else:
            if menu_pk:
                if menu_pk not in permission_menu_dict:
                    permission_menu_dict[menu_pk] = {
                        "menu_title": item["permissions__parent__title"],
                        "icon": item["permissions__parent__icon"],
                        "children": [
                            {
                                "title": item["permissions__title"],
                                "url": item["permissions__url"],
                                "order": item["permissions__order"],
                                "icon": item["permissions__icon"],
                            }
                        ],
                    }
                else:
                    permission_menu_dict[menu_pk]["children"].append({
                        "title": item["permissions__title"],
                        "url": item["permissions__url"],
                        "order": item["permissions__order"],
                        "icon": item["permissions__parent__icon"],
                    })
    # print(permission_list)
    # print(permission_menu_dict)
    # 将当前登录人的权限列表注入session中
    logger.info('将当前登录人的权限列表注入session中')
    request.session['permission_list'] = permission_list
    # 将当前登录人的菜单权限字典注入session中
    logger.info('将当前登录人的菜单权限字典注入session中')
    request.session['permission_menu_dict'] = permission_menu_dict
    logger.info('将当前登录人的项目权限注入session')
    # print(pro_list)
    request.session['pro_list'] = pro_list
    # print(request.session)
