from PlatApp.FunctionsForModels.TestCaseFunctions import RequestCaseData
from PlatApp.models import BaseSysParam

from AutoTest.InterfaceDocument.functions.ProduceTestCase import CreateCaseInfo

import logging

logger = logging.getLogger('AutoApp.app')


class CreateTestCase:
    """
    @Author: 朱孟彤
    @desc: 生成测试用例并落地数据至数据库
    """
    def __init__(self, re_data, data, user_id):
        """
        初始化数据
        :param re_data: 接口信息
        :param data: 请求数据，包含：用例生成规则、接口ID、接口名称等
        :param user_id: 操作的用户名
        """
        self.re_data = re_data
        self.data = data
        self.user_id = user_id

    def CreateTestCaseData(self):
        """
        根据接口数据创建测试用例
        :return: 返回测试用例创建结果
        """

        logger.info('根据接口数据创建测试用例')
        try:
            create_case = CreateCaseInfo(self.re_data)
            case_list = create_case.createCaseBase(self.data['case_type'])
            # logger.info(str(case_list))
            logger.info('获取接口测试用例数据')
            case_object = RequestCaseData()
            logger.info('添加测试用例集合')
            suite_context = {
                'created_by_id': int(self.user_id),
                'updated_by_id': int(self.user_id),
            }
            suite_context.update({'pro_id': int(self.re_data['project_id'])})
            type_info = BaseSysParam.objects.get(param_value='RequestCase', abandon_flag=1)
            suite_context['case_type'] = type_info.id
            suite_info = {
                'suite_name': self.re_data['re_name'],
                'description': self.re_data['re_name'] + ' --- 接口测试用例集合',
            }
            suite_result = case_object.CreateCaseSuite(suite_info, suite_context)
            suite_id = suite_result.id
        except Exception as ex:
            logger.error(ex)
            return {'status': 110, 'errorMsg': '创建用例集合异常'}
        logger.info('添加测试用例集合成功')
        logger.info('开始循环添加测试用例信息')
        case_id_list = []
        for step in case_list:
            case_info = {
                'case_name': step['case_name'],
                'description': self.re_data['re_name'] + ' --- 接口测试用例',
            }
            case_context = suite_context.copy()
            case_context['case_suite_id'] = suite_id
            case_result = case_object.CreateCaseInfo(case_info, case_context)
            try:
                case_id = case_result.id
            except Exception as ex:
                logger.error(ex)
                logger.error(case_result)
                return {'status': 110, 'errorMsg': '创建测试用例错误'}
            case_id_list.append(case_id)
            step_info = {
                'case': case_id,
                'step_type': 'execute',
                'step_id': '1',
                'execute_type': 'HTTP',
                'for_id': self.data['re_id'],
                'check_type': 10,
                'save_list': '',
                'execute_info': str(step['re_params']),
                'param_info': str(step['exp_results']),
                'description': step['case_name'],
            }
            step_result = case_object.CreateCaseStep(step_info, 'case', case_context)
            try:
                step_id = step_result.id
            except Exception as ex:
                logger.error(ex)
                logger.error(step_result)
                return {'status': 110, 'errorMsg': '创建测试步骤错误'}
            case_result.step_list.add(step_id)
            case_result.save()
            for new_case_id in case_id_list:
                suite_result.case_id.add(new_case_id)
            suite_result.save()
            logger.info('添加测试用例以及步骤成功，ID为：' + str(step_id))
        return {'status': 20, 'message': '创建测试用例成功'}