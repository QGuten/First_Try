from PlatApp.models import CaseSuiteForCaseCenter, CaseInfoForCaseCenter, CaseStepForCaseCenter
from PlatApp.SerializersForModel.CaseSerializer import CaseInfoSerializer, CaseSuiteSerializer, CaseStepSerializer


class RequestCaseData:
    """
    @Author: 朱孟彤
    @desc: 创建/更新，接口生成的测试用例
    """

    def CreateCaseSuite(self, data, context):
        """
        创建测试套件数据
        :param data: 测试套件基础数据
        :param context: 测试套件中的外键数据
        :return: 返回新增的测试套件id，或者异常信息
        """
        try:
            new_suite = CaseSuiteSerializer(data=data, context=context)
            new_suite.is_valid(raise_exception=True)
            suite_info = new_suite.save()
            return suite_info
        except Exception as ex:
            return ex

    def UpdataCaseSuite(self, data):
        """
        更新测试套件数据
        :param data: 要更新测试套件基础数据
        :return: 返回更新的测试套件id，或者异常信息
        """
        try:
            suite_info = CaseSuiteForCaseCenter.objects.get(id=data['id'])
            if data.__contains__('pro_id'):
                suite_info.pro_id = int(data['pro_id'])
            if data.__contains__('case_type'):
                suite_info.case_type_id = int(data['case_type'])
            if data.__contains__('suite_name'):
                suite_info.suite_name = str(data['suite_name'])
            if data.__contains__('description'):
                suite_info.description = str(data['description'])
            if data.__contains__('updated_by'):
                suite_info.updated_by = str(data['updated_by'])
            if data.__contains__('abandon_flag'):
                suite_info.pro_id = int(data['abandon_flag'])
            for i in data['case_list']:
                suite_info.case_id.add(i)
            suite_info.save()
            return suite_info.id
        except Exception as ex:
            return ex

    def CreateCaseInfo(self, data, context):
        """
        创建测试用例信息数据
        :param data: 测试用例基础数据
        :param context: 测试用例中的外键数据
        :return: 返回测试用例id，或者异常信息
        """
        try:
            new_case = CaseInfoSerializer(data=data, context=context)
            new_case.is_valid(raise_exception=True)
            case_info = new_case.save()
            return case_info
        except Exception as ex:
            return ex

    def UpdataCaseInfo(self, data):
        """
        更新测试用例信息数据
        :param data: 要更新测试用例基础数据
        :return: 返回更新的测试用例id，或者异常信息
        """
        try:
            suite_info = CaseInfoForCaseCenter.objects.get(id=data['id'])
            if data.__contains__('pro_id'):
                suite_info.pro_id = int(data['pro_id'])
            if data.__contains__('case_type'):
                suite_info.case_type_id = int(data['case_type'])
            if data.__contains__('case_suite'):
                suite_info.case_suite_id = int(data['case_suite'])
            if data.__contains__('case_name'):
                suite_info.case_name = str(data['case_name'])
            if data.__contains__('description'):
                suite_info.description = str(data['description'])
            if data.__contains__('updated_by'):
                suite_info.updated_by = str(data['updated_by'])
            if data.__contains__('abandon_flag'):
                suite_info.pro_id = int(data['abandon_flag'])
            for i in data['step_list']:
                suite_info.step_list.add(i)
            suite_info.save()
            return suite_info.id
        except Exception as ex:
            return ex

    def CreateCaseStep(self, data, type, context):
        """
        创建测试用例步骤信息数据，
        用例步骤中，case字段存放用例id或套件id，需要手动校验数据的准确性
        用例步骤中，for_id字段存放步骤中执行的数据id，与execute_type配合，决定检验数据，需要手动校验数据的准确性
        :param data: 步骤基础数据
        :param type: 用来区分case储存的是用例id还是套件id
        :return: 返回步骤id，或者异常信息
        """
        params_check = False
        try:
            if type == 'case' and CaseInfoForCaseCenter.objects.filter(id=data['case']):
                params_check = True
            if type == 'suite' and CaseSuiteForCaseCenter.objects.filter(id=data['case']):
                params_check = True
            if params_check:
                new_step = CaseStepSerializer(data=data, context=context)
                new_step.is_valid(raise_exception=True)
                step_info = new_step.save()
                return step_info
            else:
                return '用例ID或者套件ID不存在'
        except Exception as ex:
            return ex

    def UpdataCaseStep(self, data):
        """
        更新测试用例步骤信息数据
        :param data: 要更新测试步骤基础数据
        :return: 返回更新的测试步骤id，或者异常信息
        """
        try:
            suite_info = CaseStepForCaseCenter.objects.get(id=data['id'])
            if data.__contains__('case'):
                suite_info.case = int(data['case'])
            if data.__contains__('step_type'):
                suite_info.step_type = str(data['step_type'])
            if data.__contains__('step_id'):
                suite_info.step_id = int(data['step_id'])
            if data.__contains__('execute_type'):
                suite_info.execute_type = str(data['execute_type'])
            if data.__contains__('execute_info'):
                suite_info.execute_info = str(data['execute_info'])
            if data.__contains__('for_id'):
                suite_info.for_id = str(data['for_id'])
            if data.__contains__('check_type'):
                suite_info.check_type = str(data['check_type'])
            if data.__contains__('param_info'):
                suite_info.param_info = str(data['param_info'])
            if data.__contains__('description'):
                suite_info.description = str(data['description'])
            if data.__contains__('updated_by'):
                suite_info.updated_by = str(data['updated_by'])
            if data.__contains__('abandon_flag'):
                suite_info.pro_id = int(data['abandon_flag'])
            for i in data['step_list']:
                suite_info.step_list.add(i)
            suite_info.save()
            return suite_info.id
        except Exception as ex:
            return ex