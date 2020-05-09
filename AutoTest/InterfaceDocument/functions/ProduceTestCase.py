import copy
import logging

logger = logging.getLogger('AutoTest')


class CreateCaseInfo:
    """
    @Author: 朱孟彤
    @desc: 创建测试用例数据类
    """

    def __init__(self, data):
        """
        初始化方法，检测数据是否符合要求的dict类型，然后对数据进行处理
        :param data:
        """
        if self.checkData(data):
            logger.info('开始处理传入的接口数据')
            self.getData(data)

    def checkData(self, data):
        """
        检测传入参数类型是否正确
        :param data: 类实例化传入的参数
        :return:返回布尔类型表示检测是否通过
        """
        if isinstance(data, dict):
            logger.info('接口数据，参数检验通过')
            return True
        else:
            logger.error('接口数据，参数检验未通过')
            return False

    def getData(self, data):
        """
        处理传入参数（取出想要的参数）
        :param data:
        :return:
        """
        self.base_name = data['re_name']
        self.params = data['re_params']
        self.response = data['re_response']
        self.base_data = {
            're_id': data['id'],
            're_serial_number': data['serial_number'],
            'project_id': data['project_id'],
        }

    def createCaseBase(self, type):
        """
        生成测试用例基础数据
        :param type: 用例生成类型 list列表，包含关系判断
        :return:
        """
        logger.info('开始生成测试用例基础数据')
        case_list = []
        # 拼接正常测试用例数据，以及基础数据
        # info = self.createCaseReData(self.params)
        info = eval(self.params)
        if info:
            if 'NORMAL' in type:
            # 正常请求的测试用例
                logger.info("开始生成正常请求的测试用例")
                result = self.createCaseAssertData(True)
                case_info = {'case_name': self.base_name + ' --- 正常请求','re_params': info, 'exp_results':result}
                a = {}
                a.update(case_info)
                a.update(self.base_data)
                case_list.append(a)
            if 'INFOLACK' in type:
            # 每个字段移除，生成字段缺失用例
                logger.info("每个字段移除，生成字段缺失用例")
                for index in range(len(info)):
                    info_copy1 = copy.deepcopy(info)
                    # info_copy1 = info.copy()
                    remove_info = info_copy1.pop(index)
                    if remove_info['if_must'] == '是':
                        result = self.createCaseAssertData(False)
                    else:
                        result = self.createCaseAssertData(True)
                    case_info1 = {'case_name': self.base_name + ' --- 缺少' + remove_info['field_name'] + '字段请求','re_params': info_copy1, 'exp_results':result}
                    b = {}
                    b.update(case_info1)
                    b.update(self.base_data)
                    case_list.append(b)
            if 'INFONONE' in type:
            # 每个字段为空，生成字段为空用例
                logger.info("开始生成每个字段为空，生成字段为空用例")
                for index in range(len(info)):
                    info_copy2 = copy.deepcopy(info)
                    # info_copy2 = info.copy()
                    info_copy2[index]['value'] = "Null"
                    if info_copy2[index]['if_must'] == '是':
                        result = self.createCaseAssertData(False)
                    else:
                        result = self.createCaseAssertData(True)
                    case_info2 = {'case_name': self.base_name + ' --- ' + info_copy2[index]['field_name'] + '字段为空请求', 're_params': info_copy2,
                                 'exp_results': result}
                    c = {}
                    c.update(case_info2)
                    c.update(self.base_data)
                    case_list.append(c)
            if 'INFOERROR' in type:
            # 每个字段错误传递，生成错误传递用例
                logger.info("开始生成每个字段错误传递，生成错误传递用例")
                for index in range(len(info)):
                    info_copy3 = copy.deepcopy(info)
                    # info_copy3 = info.copy()
                    info_copy3[index]['value'] = "ErrorMessage"
                    if info_copy3[index]['if_must'] == '是':
                        result = self.createCaseAssertData(False)
                    else:
                        result = self.createCaseAssertData(True)
                    case_info3 = {'case_name': self.base_name + ' --- ' + info_copy3[index]['field_name'] + '字段错误请求', 're_params': info_copy3,
                                 'exp_results': result}
                    d = {}
                    d.update(case_info3)
                    d.update(self.base_data)
                    case_list.append(d)
        else:
            result = self.createCaseAssertData(True)
            case_info = {'case_name': self.base_name + ' --- 正常请求', 're_params': info, 'exp_results': result}
            a = {}
            a.update(case_info)
            a.update(self.base_data)
            case_list.append(a)
        return case_list


    def createCaseReData(self, data):
        """
        数据生成拼接为测试用例请求数据的基础数据
        :return:
        """
        if data == '无':
            return None
        else:
            re_key = ['name', 'type', 'if_must', 'des']
            # 测试用例请求数据的基础数据
            logger.info("生成测试用例请求数据的基础数据")
            re_params = []
            # for data_info in eval(data)['td']:
            for data_info in eval(data):
                d = {
                    re_key[0]: data_info[0],
                    re_key[1]: data_info[1],
                    re_key[2]: data_info[2],
                    re_key[3]: data_info[3],
                }
                re_params.append(d)
            return re_params

    def createCaseAssertData(self, result):
        """
        数据生成拼接为测试用例字段断言数据
        :param result: 错误还是正确的断言
        :return:
        """
        # ex_error = [
        #     {'name': 'id', 'des': '请求ID，每次请求生成的唯一ID'},
        #     {'name': 'code', 'des': '业务码，唯一ID'},
        #     {'name': 'status', 'des': '状态码，200->ok,210->notice,500->error'},
        #     {'name': 'message', 'des': '提示/错误信息'},
        #     {'name': 'error', 'des': 'ERROR'},
        #     {'name': 'data', 'des': '响应数据'},
        # ]
        assert_params = []
        assert_params.append(self.response)
        # if result:
        #     assert_params.append({
        #         'field_name': 'status', 'field_type': 'int', 'if_must': '1', 'field_desc': '200->ok,210->notice,500->error','exp_results': 200
        #     })
        # else:
        #     assert_params.append(
        #         {'field_name': 'status', 'field_type': 'int', 'if_must': '1', 'field_desc': '状态码，200->ok,210->notice,500->error','exp_results':[210,405,500]}
        #     )
        #     assert_params.append(
        #         {'field_name': 'error', 'field_type': 'string', 'if_must': '1', 'field_desc': 'ERROR','exp_results': 'ERROR'}
        #     )
        # return assert_params
        return self.response


if __name__ == '__main__':
    test_case_data = {'id': 2235, 'serial_number': 'IIU7kt', 're_name': '批量查询员工头像',
                      're_path': '{domain}/service/v1avatar/list',
                      're_method': 'GET', 're_other': '{}', 'project_id': 377,
                      're_params': "{'th': ['字段', '类型', '必填', '描述'],'td': [['enterprise_id', 'int', '是', '企业id'], ['mem_uids', 'array', '否', '员工id集合（一维数组）']]}",
                      're_response': "{'th': ['字段', '类型', '描述'], 'td': [['enterprise_id', 'int', '企业id'], ['mem_uid', 'string', '员工ring', '头像']]}",
                      'ex_response': '{ "data": [ { "enterprise_id": 1, "mem_uid": "96BE3FF47F00000154867D7E913523F7", "avatar": "http://p.qlogo.cn/bizmail/UBxIswgb0icArLiaOEF9fd6HyLF06J6YaIOB0DMdqO8N20wa8gay0A/0" } ] }',
                      'error_response': '无', 'edition': '', 'developer': '王欢', 'if_update': 1,
                      'created_by': 'zhumengtong', 'updated_by': 'zhumengtong', 'description': None, 'abandon_flag': 1}
    case_type = ['NORMAL','INFOLACK','INFONONE','INFOERROR']
    case_info = CreateCaseInfo(test_case_data)
    a = case_info.createCaseBase(case_type)
    [print(b) for b in a]