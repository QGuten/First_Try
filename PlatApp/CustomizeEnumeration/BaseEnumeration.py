from enum import Enum


class BaseEnumeration(Enum):
    """
    @Author: 朱孟彤
    @desc: 基础配置/页面，相关枚举
    """
    CREATE_PROJECT_ERROR = {
        'errCode': 13001, 'errMsg': "添加项目配置失败"
    }

    UPDATE_PROJECT_ERROR = {
        'errCode': 13002, 'errMsg': "更新项目配置失败"
    }

    PROJECT_ID_ERROR = {
        'errCode': 13003, 'errMsg': "请求参数错误"
    }

    CREATE_SYS_PARAM_ERROR = {
        'errCode': 13004, 'errMsg': "添加系统参数配置失败"
    }

    UPDATE_SYS_PARAM_ERROR = {
        'errCode': 13005, 'errMsg': "更新系统参数配置失败"
    }

    SYS_PARAM_ID_ERROR = {
        'errCode': 13006, 'errMsg': "请求参数错误"
    }

    GET_MODEL_FROM_PRO_ERROR = {
        'errCode': 13007, 'errMsg': "获取模块列表异常，请稍后再试"
    }

    CREATE_SYS_VERSION_ERROR = {
        'errCode': 13008, 'errMsg': "新增版本配置错误"
    }

    UPDATE_SYS_VERSION_ERROR = {
        'errCode': 13009, 'errMsg': "更新版本配置错误"
    }

    CREATE_PROJECT_DATA_ERROR = {
        'errCode': 13010, 'errMsg': "该项目配置已经添加，请勿重复添加！"
    }

    CREATE_SYS_VERSION_REPEAT_ERROR = {
        'errCode': 13011, 'errMsg': "该项目版本号已经添加，请勿重复添加！"
    }

    CREATE_SYS_PARAM_REPEAT_ERROR = {
        'errCode': 13012, 'errMsg': "该系统参数配置已经添加，请勿重复添加！"
    }