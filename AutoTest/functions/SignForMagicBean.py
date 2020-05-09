# from AutoTest.Src.common.JarRequests import JarRequests
from AutoTest.Common.PathHandle import PathGet
from AutoTest.Common.TestConfig import IniOperation

from jpype import *
import jpype


class Sign:
    """
    @Author: 朱孟彤
    @desc: 调用验签
    """

    def __init__(self):
        self.params = {
            'appkey': 'str',
            'secretkey': 'str',
            'url': 'str',
            'param': 'str',
            'timestamp': 'int'
        }

    def __getJarPath(self, file_name):
        pathObj = PathGet()
        path = pathObj.getfile(pathObj.getfile(pathObj.getpath()))
        path = pathObj.addpath(path, file_name)
        return path

    def __getConfig(self):
        data = {}
        config_path = self.__getJarPath('Config')
        self.ini_obj = IniOperation()
        self.ini_path = "{}/{}".format(config_path, 'SignConfig.ini')
        self.ini_obj.OpenIni(self.ini_path)
        for key, value in self.params.items():
            data[key] = self.ini_obj.GetOption('sign_info', key, value)
        data['jar_name'] = self.ini_obj.GetOption('config', 'jar_name', 'str')
        data['class_name'] = self.ini_obj.GetOption('config', 'class_name', 'str')
        return data

    def get_signature(self):

        data = self.__getConfig()
        print(data)

        if jpype.isJVMStarted():
            jpype.shutdownJVM()

        try:
            jvmPath = jpype.getDefaultJVMPath()
            jar_path = self.__getJarPath('JavaJar')
            full_path = jar_path + '/' + data['jar_name']
            jpype.startJVM(jvmPath, '-ea', "-Djava.class.path={}".format(full_path))
            JDClass = JClass(data['class_name'])
            jd = JDClass()
            re_data = jd.generateSignOfPost(data['appkey'], data['secretkey'], data['url'], str(data['param']),
                                            int(data['timestamp']))
            jpype.shutdownJVM()
            print(re_data)
            self.ini_obj.NewOption('result', 'info', re_data)
            self.ini_obj.WriteIni(self.ini_path)
            return {'code': 20, 'data': re_data}
        except Exception as ex:
            jpype.shutdownJVM()
            return {'code': 110, 'data': ex}


if __name__ == '__main__':
    jvmPath = jpype.getDefaultJVMPath()
    s = Sign()
    s.get_signature()
