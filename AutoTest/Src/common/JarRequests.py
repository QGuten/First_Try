import jpype
from jpype import *
from AutoTest.Common.PathHandle import PathGet


class JarRequests:
    """
    @Author: 朱孟彤
    @desc: 使用jpype调用Jar包方法封装
    """
    def __init__(self):
        self.if_start = False

    def __getJarPath(self):
        pathObj = PathGet()
        path = pathObj.getfile(pathObj.getfile(pathObj.getpath()))
        path = pathObj.addpath(path, 'JavaJar')
        return path

    def startJvm(self, jar_name, class_name):
        if jpype.isJVMStarted():
            print(1111111)
            jpype.shutdownJVM()
        jvmPath = jpype.getDefaultJVMPath()
        jar_path = self.__getJarPath()
        jpype.startJVM(jvmPath, '-ea', "-Djava.class.path={}/{}".format(jar_path, jar_name))
        JDClass = JClass(class_name)
        self.jd = JDClass()
        return self.jd

    def closeJvm(self):
        jpype.shutdownJVM()

# if __name__ == '__main__':
#     jar = JarRequests()
#     jar.startJvm('sign.jar')
#     # jar.createJd('com.test.TestGenerateSign')
#
#     JDClass = JClass("com.test.TestGenerateSign")
#     jd = JDClass()
#     shutdownJVM()
