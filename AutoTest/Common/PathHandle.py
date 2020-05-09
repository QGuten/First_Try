# -*- coding: utf-8 -*-
# @Time    : 2018/09/29 17:00
# @Author  : 朱孟彤
# @File    : PathHandle.py
# @desc:路径操作封装类
import os


class PathGet:
    """
    @Author: 朱孟彤
    @desc: 路径操作封装类
    """

    def getpath(self):
        """
        获取当前脚本的真实路径
        :return: 当前脚本的真实路径
        """
        cur_path = os.path.realpath(__file__)
        return cur_path

    def getname(self, cur_path):
        """
        根据路径，获得脚本名称
        :param cur_path: 需要获取脚本名称的路径
        :return: 返回脚本名称
        """
        name = os.path.basename(cur_path)
        return name

    def getfile(self, cur_path):
        """
        根据路径，获取的脚本文件夹路径，
        若传入的是一个路径，则获取的就是上一级目录
        若传入的是带有文件名的路径，则获取的就是文件所在的文件夹目录
        :param cur_path: 需要获取脚本文件夹的完整路径
        :return: 返回文件夹路径
        """
        file_path = os.path.dirname(cur_path)
        return file_path

    def addpath(self, path, *str):
        """
        拼接文件路径
        :param path: 原始路径
        :param str: 需要拼接的路径
        :return: 拼接完成的路径
        """
        param = "/".join(i for i in str)
        ta_path = os.path.join(path, param)
        return ta_path

    def pathtrue(self, path):
        """
        判断文件夹是否存在
        :param path: 需要判断的文件夹地址
        :return: 返回判断结果
        """
        t = os.path.exists(path)
        return t

    def createfile(self, path):
        """
        创建文件路径
        :param path: 创建的路径
        :return: 返回创建结果
        """
        try:
            os.mkdir(path)
        except:
            return "create error"
        else:
            return True
