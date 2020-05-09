import logging

from django.forms import model_to_dict
from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from PlatApp.models import OpsUser, Role, Menu, ProjectForBase

logger = logging.getLogger('AutoApp.app')


class LoginIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 登录页
    """

    template_name = "login.html"


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UserIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 用户列表页
    """

    template_name = "UserCenter/UserList.html"

    def get_context_data(self, **kwargs):
        # 获取角色列表信息
        RoleList = Role.objects.filter(abandon_flag=1)
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UserInfo(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 用户个人信息页
    """

    template_name = "UserCenter/UserInfo.html"

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        try:
            user_info = OpsUser.objects.get(id=user_id)

            roles = "，".join(i.title for i in user_info.role.all())
            user_pros = "，".join(j.project_name for j in user_info.pro.all())

            # 获取角色列表信息
            RoleList = Role.objects.filter(abandon_flag=1)
        except Exception as ex:
            logger.error('用户资料获取失败')
            logger.error(ex)
            user_info = '数据异常'
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AddUserIndex(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 添加用户页
    """

    template_name = "UserCenter/AddUser.html"
    model = Role

    def get_context_data(self, **kwargs):
        """
        重写方法，获取页面需要展示的角色列表信息
        :param kwargs:
        :return:
        """
        # 获取项目配置
        pro_list = ProjectForBase.objects.filter(parent__id__isnull=True, abandon_flag=1)
        # 获取角色列表信息
        RoleList = Role.objects.filter(abandon_flag=1)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class JurisdictionList(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 权限管理，菜单列表页
    """

    template_name = "UserCenter/JurisdictionList.html"

    def get_context_data(self, **kwargs):
        """
        重写方法，获取页面需要展示的权限配置信息
        :param kwargs:
        :return:
        """
        # 获取菜单列表
        menu_list = Menu.objects.filter(parent__isnull=True, abandon_flag=1)
        return locals()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class RoleList(TemplateView):
    """
    @Author: 朱孟彤
    @desc: 权限管理，角色列表页
    """

    template_name = "UserCenter/RoleList.html"

    def get_context_data(self, **kwargs):
        """
        重写方法，获取页面需要展示的权限配置信息
        :param kwargs:
        :return:
        """
        # 获取权限列表
        permission_list = Menu.objects.exclude(url__in='#', abandon_flag=1)
        return locals()
