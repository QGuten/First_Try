import logging
import assertpy
import demjson

logger = logging.getLogger('AutoTest')


class GetData:
    """
    @Author: 朱孟彤
    @desc: json多层中获取数据
    """

    def __init__(self):
        self.res_list = []
        self.res_dict = {}

    def getDataForList(self, data, key_list: list):
        """
        在数据中提取出想要的数据
        :param data 数据源
        :param key_list 所取数据的key
        :return: 返回提取出的数据
        """
        for key in key_list:
            return self.__get_value_form_dict(data, key, 'list')

    def getDataForKey(self, data, key):
        """
        在数据中提取出想要的数据
        :param data 数据源
        :param key 所取数据的key
        :return: 返回提取出的数据
        """
        result_data = self.__handle_dict(data)
        return self.__get_value_form_dict(result_data, key, 'dict')

    def __get_value_form_dict(self, data, key, re_type):
        """
        字典中提取
        :param data: 数据源
        :param key: 数据key
        :return: 返回数据源和数据key组合的字典
        """
        if not isinstance(data, dict):
            return data + "is not dict"
        elif key in data.keys():
            if re_type == "dict":
                self.res_dict[key] = data[key]
            elif re_type == "list":
                self.res_list.append({key: data[key]})
            return {key: data[key]}
        else:
            for value in data.values():
                if isinstance(value, dict):
                    self.__get_value_form_dict(value, key, re_type)
                elif isinstance(value, (list, tuple)):
                    self.__get_value_form_list(value, key, re_type)

    def __get_value_form_list(self, data, key, re_type):
        """

        :param key:
        :param tdict:
        :param tem_list:
        :return:
        """
        for value in data:
            if isinstance(value, (list, tuple)):
                self.__get_value_form_list(value, key, re_type)
            elif isinstance(value, dict):
                self.__get_value_form_dict(value, key, re_type)

    def __handle_dict(self, data):
        # null值预处理（解决eval问题）
        global null
        null = 'null'
        # false值预处理（解决eval问题）
        global false
        false = 'false'
        # true值预处理（解决eval问题）
        global true
        true = 'true'
        if isinstance(data, dict):
            results_dict = eval("{}".format(data))
        elif isinstance(data, list):
            results_dict = [eval("{}".format(i)) for i in data]
        else:
            # 转换为字典方式
            results = demjson.decode(data)
            results_dict = eval("{}".format(results))
        return results_dict