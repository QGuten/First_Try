# 获取平台需要显示的一些基础信息


def base_info(request):
    """
    @Author: 朱孟彤
    @desc: 添加用户名和权限，以及基础信息，到session中。
    :param request:
    :return:
    """
    title = 'Beantech 测试平台'
    header = 'Beantech 测试平台'
    try:
        if_login = 1
        username = request.user.last_name + request.user.first_name
        if_admin = request.user.is_superuser
    except Exception as ex:
        if_login = 0
        if_admin = None
        username = '您还未登录，请先登录'
    return {'username': username, 'title': title, 'header': header, 'if_login': if_login, 'if_admin': if_admin}
