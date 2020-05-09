from enum import Enum


class JobCenterEnumeration(Enum):
    """
    @Author: 朱孟彤
    @desc: 测试任务、测试报告，相关枚举
    14001
    """
    CREATE_JOB_ERROR = {
        'code': 16001, 'errMsg': "任务创建失败"
    }

    GET_INFO_ERROR = {
        'code': 16002, 'errMsg': "请求参数错误"
    }

    SYS_JOB_ERROR = {
        'code': 16003, 'errMsg': "系统异常，请稍后再试"
    }

    GET_JOB_INFO_ERROR = {
        'code': 16004, 'errMsg': "查询任务信息错误"
    }

    CREATE_SUB_JOB_ERROR = {
        'code': 16005, 'errMsg': "任务创建失败"
    }

    EXE_SUB_JOB_ERROR = {
        'code': 16006, 'errMsg': "执行子任务失败"
    }

    GET_REPORT_CASE_INTO_ERROR = {
        'code': 16007, 'errMsg': "获取报告用例步骤执行详情失败"
    }

    UPDATE_JOB_STATE_ERROR = {
        'code': 16008, 'errMsg': "更新父任务状态失败"
    }
    UPDATE_JOB_DATA_STATE_ERROR = {
        'code': 16009, 'errMsg': "更新父任务数据状态失败"
    }

    UPDATE_SUB_JOB_STATE_ERROR = {
        'code': 16010, 'errMsg': "更新子任务状态失败"
    }
    UPDATE_SUB_JOB_DATA_STATE_ERROR = {
        'code': 16011, 'errMsg': "更新子任务数据状态失败"
    }
    UPDATE_IT_STATE_ERROR = {
        'code': 16012, 'errMsg': "更新迭代失败"
    }
    EXE_IT_JOB_ERROR = {
        'code': 16013, 'errMsg': "执行迭代失败"
    }
