# -*- coding: utf-8 -*-
# Author 朱孟彤
# time：20180929
import telnetlib
import socket
import demjson
import logging

logger = logging.getLogger('AutoTest')


class Dubbo(telnetlib.Telnet):
    """
    @Author: 朱孟彤
    @desc: Dubbo接口请求封装
    """

    prompt = 'dubbo>'

    def __init__(self, host=None, port=0,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        super().__init__(host, port)
        self.write(b'\n')

    def command(self, flag, str_=""):
        data = self.read_until(flag.encode())
        self.write(str_.encode() + b"\n")
        return data

    def invoke_list(self, service_name, method_name, a, b):
        '''支持所有参数类型的dubbo接口调用'''
        command_str = "invoke {0}.{1}({2},[3])".format(service_name, method_name, a, b)
        self.command(Dubbo.prompt, command_str)
        data = self.command(Dubbo.prompt, "")
        data = demjson.encode(data.decode(encoding='gb2312', errors='ignore').split('\n')[0].strip())
        return data

    def invoke(self, service_name, method_name, *arg):
        '''支持所有参数类型的dubbo接口调用'''
        if isinstance(arg, (dict,)):
            logger.info('接口请求参数为对象')
            command_str = "invoke {0}.{1}({2})".format(service_name, method_name, demjson.encode(arg))
        elif arg == 'null' or arg == '':
            logger.info('接口请求参数为空')
            command_str = "invoke {0}.{1}()".format(service_name, method_name)
        # elif isinstance(arg, (tuple, list)):
        elif isinstance(arg, (tuple, )):
            logger.info('接口请求参数为元组/数组')
            param = ",".join(str(i) for i in arg)
            command_str = "invoke {0}.{1}({2})".format(service_name, method_name, param)
        else:
            logger.info('接口请求参数不是对象、空、元组/数组')
            command_str = "invoke {0}.{1}({2})".format(service_name, method_name, arg)
        self.command(Dubbo.prompt, command_str)
        data = self.command(Dubbo.prompt, "")
        data = demjson.encode(data.decode(encoding='gb2312', errors='ignore').split('\n')[0].strip())
        logger.info('请求结果为：%s' % data)
        return data

    def invoke_json(self, data):
        '''支持所有参数类型的dubbo接口调用'''
        service_name = data['service_name']
        method_name = data['method_name']
        params = data['params']
        if isinstance(params, (dict,)):
            command_str = "invoke {0}.{1}({2})".format(service_name, method_name, demjson.encode(params))
        elif params == 'null' or params == '':
            command_str = "invoke {0}.{1}()".format(service_name, method_name,)
        elif isinstance(params, (tuple, list)):
            param = ",".join(str(i) for i in params)
            command_str = "invoke {0}.{1}({2})".format(service_name, method_name, param)
        else:
            command_str = "invoke {0}.{1}({2})".format(service_name, method_name, params)
        self.command(Dubbo.prompt, command_str)
        result = self.command(Dubbo.prompt, "")
        result = demjson.encode(result.decode(encoding='gb2312', errors='ignore').split('\n')[0].strip())
        return result

    def findinterfaces(self):
        '''创建实例化对象后，调用可以获得所有的interface'''
        method = 'ls'
        command_str = "{0}".format(method)
        self.command(Dubbo.prompt, command_str)
        data = self.command(Dubbo.prompt, "")
        interfaces = demjson.encode(data.decode(encoding='gb2312', errors='ignore')).strip('"').split('\\r\\n')
        interfaces.pop()
        return interfaces

    def findmethods(self, interface):
        '''根据interface获取所有的method'''
        command = 'ls'
        command_str = "{0} {1}".format(command, interface)
        self.command(Dubbo.prompt, command_str)
        data = self.command(Dubbo.prompt, "")
        methods = demjson.encode(data.decode(encoding='gb2312', errors='ignore')).strip('"').split('\\r\\n')
        methods.pop()
        return methods

    def findmethods_info(self, interface):
        '''根据interface获取所有的method，包含详细信息'''
        command = 'ls -l'
        command_str = "{0} {1}".format(command, interface)
        self.command(Dubbo.prompt, command_str)
        data = self.command(Dubbo.prompt, "")
        methods = demjson.encode(data.decode(encoding='gb2312', errors='ignore')).strip('"').split('\\r\\n')
        methods.pop()
        info = []
        for i in methods:
            a = i.split()
            c = a.pop(1)
            b = c.split('(')
            b[1] = b[1].strip(')')
            if ',' in b[1]:
                b[1] = b[1].split(',')
            a = a + b
            info.append(a)
        return info

# 处理json数据
    def resultjson(self, results):
        '''把返回的callbackFunName结果转换为字典'''

        # null值预处理（解决eval问题）
        global null
        null = 'null'
        # false值预处理（解决eval问题）
        global false
        false = 'false'
        # true值预处理（解决eval问题）
        global true
        true = 'true'
        # 转换为字典方式
        results = demjson.decode(results)

        results_dict = eval("{}".format(results))
        return results_dict

    def resultJudge(self,results):
        """判断返回结果中是否有列表中的内容，如果有，则返回请求失败"""
        errorMsg = ""
        fail = ["Failed","No such method"]
        for i in fail:
            result = i in results
            if result:
                errorMsg = "Dubbo requests failed!"
                break
        return errorMsg


if __name__ == '__main__':
    conn = Dubbo("10.50.22.22", 11124)
    data = conn.invoke("com.aldb.magicmall.akc.activity.srv.ActInfoSynService", "processLiveInfoSyn")
    print(data)
    conn.close()