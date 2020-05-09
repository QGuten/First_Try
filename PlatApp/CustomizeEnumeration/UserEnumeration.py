from enum import Enum


class UserEnumeration(Enum):
    """
    @Author: 朱孟彤
    @desc: 角色用户操作，相关枚举
    """
    SIGN_IN_ERROR_2 = "登录失败"

    SIGNOUT_ERROR = {
        'errCode': 12002, 'errMsg': "退出错误"
    }

    SIGN_IN_ERROR_1 = {
        'errCode': 12003, 'errMsg': "用户名或密码错误"
    }

    REGISTER_USERNAME_ERROR = {
        'errCode': 12004, 'errMsg': "请输入您的用户名"
    }

    REGISTER_ERROR = {
        'errCode': 12005, 'errMsg': "注册失败"
    }

    REGISTER_USERNAME_FORGET_ERROR = {
        'errCode': 12006, 'errMsg': "用户名已存在，请选择忘记密码"
    }

    REGISTER_EMAIL_FORGET_ERROR = {
        'errCode': 12007, 'errMsg': "邮箱已经注册，请选择找回用户名和密码"
    }

    REGISTER_PHONE_FORGET_ERROR = {
        'errCode': 12008, 'errMsg': "手机号已经注册，请选择找回用户名和密码"
    }

    REGISTER_USER_TYPE_ERROR = {
        'errCode': 12009, 'errMsg': "请求参数错误"
    }

    CREATE_MENU_ERROR = {
        'errCode': 12010, 'errMsg': "创建失败"
    }

    SET_PASSWORD_ERROR = {
        'errCode': 12011, 'errMsg': "重置密码失败"
    }

    PASSWORD_INPUT_ERROR = {
        'errCode': 12012, 'errMsg': "两次输入密码不一致，请重新输入"
    }

    MOBIlE_NUMBER_ERROR = {
        'errCode': 12013, 'errMsg': '手机号码格式错误，请确认'
    }

    EMAIL_NUMBER_ERROR = {
        'errCode': 12014, 'errMsg': '邮箱格式错误，请确认'
    }

    MOBILE_DOUBLE_ERROR = {
        'errCode': 12015, 'errMsg': '手机号已被注册'
    }

    EMAIL_DOUBLE_ERROR = {
        'errCode': 12016, 'errMsg': "邮箱已被注册"
    }

    UPDATE_USER_INFO_ERROR = {
        'errCode': 12017, 'errMsg': "用户信息更新失败，请稍后再试！"
    }

    GET_INFO_ERROR = {
        'errCode': 12018, 'errMsg': "信息获取失败，请稍后再试！"
    }

    USER_ID_ERROR = {
        'errCode': 12019, 'errMsg': "无此用户，请检查您的请求参数！"
    }