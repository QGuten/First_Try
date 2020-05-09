from enum import Enum


class ResourceEnumeration(Enum):
    """
    @Author: 朱孟彤
    @desc: 资源库，相关枚举
    """
    CREATE_CONFIG_ERROE = {
        'errCode': 15001, 'errMsg': "添加资源库配置错误"
    }
    UPDATE_CONFIG_ERROE = {
        'errCode': 15002, 'errMsg': "更新资源库配置错误"
    }
    CONFIG_ID_ERROR = {
        'errCode': 15003, 'errMsg': "请求参数错误"
    }

    GET_RE_DOCS_ERROR = {
        'errCode': 15004, 'errMsg': "接口文档解析错误"
    }
    CREATE_CASE_ERROR = {
        'errCode': 15005, 'errMsg': "测试用例生成失败"
    }
    RE_ERROR = {
        'errCode': 15006, 'errMsg': "请求异常"
    }

    CREATE_REQUEST_ERROR = {
        'errCode': 15007, 'errMsg': "创建接口错误"
    }

    GET_REQUEST_LIST_ERROE = {
        'errCode': 15008, 'errMsg': "获取接口列表错误"
    }

    SYS_ERROE = {
        'errCode': 15009, 'errMsg': "系统异常，请稍后重试"
    }

    UPDATE_REQUEST_ERROR = {
        'errCode': 15010, 'errMsg': "接口信息更新异常"
    }

    REQUEST_ID_ERROR = {
        'errCode': 15011, 'errMsg': "接口数据不存在"
    }

    RE_PATH_ERROR = {
        'errCode': 15012, 'errMsg': "该接口地址已经添加，请勿重复添加！"
    }

    CONFIG_REPEAT_ERROE = {
        'errCode': 15013, 'errMsg': "该资源库配置已经添加，请勿重复添加！"
    }


