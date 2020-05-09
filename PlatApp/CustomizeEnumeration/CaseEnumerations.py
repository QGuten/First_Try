from enum import Enum


class CaseEnumeration(Enum):
    """
    @Author: 朱孟彤
    @desc: 测试用例、测试套件，相关枚举
    14001
    """
    GET_INFO_ERROR = {
        'code': 14001, 'errMsg': "请求参数错误"
    }
    CREATE_CASE_ERROR = {
        'code': 14002, 'errMsg': "创建用例错误"
    }
    CREATE_CASE_INFO_ERROR = {
        'code': 14003, 'errMsg': "创建测试用例信息错误"
    }
    CREATE_CASE_STEP_ERROR = {
        'code': 14004, 'errMsg': "创建测试用例步骤错误"
    }
    UPDATE_CASE_ERROR = {
        'code': 14005, 'errMsg': "更新测试用例信息失败"
    }
    UPDATE_CASE_STEP_ERROR = {
        'code': 14006, 'errMsg': "更新测试步骤信息失败"
    }
    UPDATE_SUITE_ERROR = {
        'code': 140057, 'errMsg': "更新测试集合信息失败"
    }
