import logging

from django.core.cache import cache

from AutoTest.Src.common.RunMethod import Http
from AutoTest.Src.common.AssertMethod import GetData

logger = logging.getLogger('AutoTest')


class ExeStep:
    """
    @Author: 朱孟彤
    @desc: 按照步骤类型执行分发
    """

    def __init__(self, job_info, cache_key):
        # 获取任务执行时需要的参数：域名、header、验签参数
        self.cache_key = cache_key
        self.re_connet = Http(job_info, cache_key)

    def runStep(self, data: dict, info_key: str):
        """
        按照步骤信息分发执行
        :return:
        """
        logger.info("---> 进入测试步骤执行类型分发执行")
        if data['execute_type'] == 'HTTP':
            return self.__exeHttp(data, info_key)
        elif data['execute_type'] == 'Socket':
            pass
        elif data['execute_type'] == 'Dubbo':
            pass

    def __exeHttp(self, data: dict, info_key: str):

        logger.info("---> 步骤执行类型为HTTP，开始执行")

        key_header = info_key[:-9]

        result = self.re_connet.getRun(data, key_header)

        logger.info("---> 执行完毕，开始处理返回值数据：{}".format(result))

        logger.info("---> 添加执行完毕数据信息至redis缓存")

        key = info_key.replace('step_info', 'result')

        if isinstance(result, dict):
            cache.set(key, result, timeout=9999999999)
        elif isinstance(result, str):
            cache.set(key, {'errorMsg': result}, timeout=9999999999)
        else:
            cache.set(key, {'errorMsg': result}, timeout=9999999999)

        logger.info("---> 开始进行返回值校验")
        if isinstance(result, dict):
            # case_info['result']
            result_true = self.__resultDataCompared(result, data['result'])
            if result_true['code'] == 20:
                logger.info("---> 开始进行储存参数存储")
                if data['save_list']:
                    re_save = self.__saveListStoreFromCache(data['save_list'], result['text'])
                    if re_save['code'] == 20:
                        return {'code': 20, 'msg': '步骤执行成功，储存参数存储成功', 'result_key': key}
                    else:
                        return {'code': 20, 'msg': '步骤执行成功，储存参数存储失败', 'result_key': key}
                else:
                    return {'code': 20, 'msg': '步骤执行成功，无储存参数', 'result_key': key}
            else:
                return {'code': 110, 'msg': '步骤执行失败', 'result_key': key}
            pass
        else:
            logger.error("步骤执行失败: {}".format(result))
            return {'code': 110, 'msg': '步骤执行失败', 'result_key': key}

    def __resultDataCompared(self, exe_result: dict, expect_result: dict):

        if str(exe_result["http_status_code"]) == '200':

            logger.info("当前请求Http状态码为：{}".format(exe_result["http_status_code"]))

            re_info = exe_result['text']

            if_pass = True

            try:
                logger.info("开始返回值校验，执行数据：{}，校验数据：{}".format(re_info, expect_result))

                get_data_func = GetData()

                for re_key, re_value in expect_result.items():
                    if re_key != "status" and re_info.__contains__(re_key):
                        get_data_func.getDataForKey(re_info, re_key)
                        end_value = get_data_func.res_dict[re_key]
                        if str(end_value) != str(re_value):
                            if_pass = False
                            break

                if if_pass:
                    logger.info("返回值校验通过")
                    return {'code': 20, 'msg': '返回值校验通过'}
                else:
                    logger.info("返回值校验通过")
                    return {'code': 110, 'msg': '返回值校验失败'}

            except Exception as e:
                logger.error("返回值校验失败: {}".format(e))
                return {'code': 110, 'msg': '返回值校验失败'}
        else:
            logger.error("Http状态码校验失败: {}".format(exe_result["http_status_code"]))
            return {'code': 110, 'msg': '返回值校验失败'}

    def __saveListStoreFromCache(self, save_list: str, exe_result: dict):

        logger.info("---> 获取缓存池中的数据")
        cache_info = cache.get(self.cache_key)

        if not cache_info:
            cache_info = {}

        try:

            logger.info("---> 开始处理储存参数")
            get_result_func = GetData()

            if ';' in save_list:
                save_list = [i for i in save_list.split(';') if i != '']
                # result_data = eval(res["text"])
                for param in save_list:
                    if ':' in param:
                        one_list = param.split(':')
                        logger.info("---> 存储参数名字：{}，别名：{}".format(one_list[0], one_list[1]))
                        get_result_func.getDataForKey(exe_result["data"], one_list[0])
                        if len(get_result_func.res_dict) != 0:
                            cache_info[one_list[1]] = get_result_func.res_dict[one_list[0]]
                    else:
                        logger.info("---> 存储参数名字：{}".format(param))
                        get_result_func.getDataForKey(exe_result, param)
                        if get_result_func.res_dict:
                            cache_info[param] = get_result_func.res_dict[param]
            else:
                find_key = save_list
                logger.info("---> 存储参数名字：{}".format(find_key))
                get_result_func.getDataForKey(exe_result, find_key)
                if get_result_func.res_dict:
                    cache_info[find_key] = get_result_func.res_dict[find_key]

            logger.info("---> 存储已获取的参数：{}".format(cache_info))
            cache.set(self.cache_key, cache_info, timeout=9999999999)
            return {'code': 20, 'msg': '处理储存参数成功'}

        except Exception as e:
            logger.info("---> 存储已获取的参数：{}".format(cache_info))
            cache.set(self.cache_key, cache_info, timeout=9999999999)
            logger.error("处理储存参数失败: {}".format(e))
            return {'code': 110, 'msg': '处理储存参数失败'}
