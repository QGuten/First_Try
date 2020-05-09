from django.urls import path, include

from rest_framework import routers

from PlatApp.PageForApp import UsersPages
from PlatApp.RestFulForApp import UsersRestFul

router = routers.DefaultRouter()    # 创建路由对象
# router.register(r'userlist', UsersRestFul.GetUserList, basename='userlist')
# router.register(r'getmenulist', UsersRestFul.GetMenuList, basename='GetMenuList')
# router.register(r'GetPermissionList', UsersRestFul.GetPermissionList, basename='GetPermissionList')
# router.register(r'getrolelist', UsersRestFul.GetRoleList, basename='GetRoleList')


app_name = "UserCenter"

urlpatterns = [
    # 页面相关路由配置
    # path('', UsersPages.LoginIndex.as_view(), name='login'),
    path('user/index/', UsersPages.UserIndex.as_view(), name='UserIndex'),
    path('user/info/', UsersPages.UserInfo.as_view(), name='UserInfo'),
    path('user/create/', UsersPages.AddUserIndex.as_view(), name='AddUserIndex'),

    path('jurisdiction/index/', UsersPages.JurisdictionList.as_view(), name='JurisdictionList'),
    path('role/index/', UsersPages.RoleList.as_view(), name='RoleList'),

    # 接口相关页面配置
    path('api/singin/', UsersRestFul.SingIn.as_view(), name='SingIn'),
    path('api/singout/', UsersRestFul.SignOut.as_view(), name='SingOut'),
    path('api/setpassword/', UsersRestFul.SetPassword.as_view(), name='SetPassword'),

    path('api/users/', UsersRestFul.UsersApi.as_view(), name='UsersApi'),
    path('api/menus/', UsersRestFul.MenuApi.as_view(), name='MenuApi'),
    path('api/roles/', UsersRestFul.RoleApi.as_view(), name='RoleApi'),

    # restframework 接口路由导入
    # path('api/', include(router.urls)),
]
