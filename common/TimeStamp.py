# -*- coding: utf-8 -*-
# @Time    : 2018/09/29 17：00
# @Author  : 朱孟彤
# @File    : TimeStamp.py
# @desc:时间操作方法类
import time


class TimeOperation:
    """
    @Author: 朱孟彤
    @desc: 时间操作方法类
    """

    def timeconver(self, timestr, formatstr="%Y-%m-%d %H:%M:%S"):
        """
        转换不标准时间格式，为指定格式
        :param timestr: 时间字符串
        :param formatstr: 时间格式字符串
        :return: 返回转换完成的时间
        """
        timearray = time.strptime(timestr, formatstr)
        return timearray

    def timestamp(self, timestr):
        """
        时间格式转换为时间戳
        :param timestr: 时间字符串
        :return: 返回时间戳
        """
        stamp = time.mktime(timestr)
        return stamp

    def timechange(self, timestamp):
        """
        时间戳转换为时间格式
        :return: 正常格式的时间
        """
        t = time.localtime(timestamp)
        return t

    def getnowstamp(self):
        """
        获取当前时间
        :return: 返回当前时间的时间戳
        """
        now = time.time()
        return now

    def getnowtime(self, formatstr="%Y-%m-%d %H:%M:%S"):
        """
        获取当前时间，格式：年月日时分秒
        :param formatstr: 时间格式
        :return: 返回当前时间
        """
        a = self.getnowstamp()
        b = self.timechange(a)
        c = time.strftime(formatstr, b)
        return c

    def getnowdate(self, formatstr="%Y-%m-%d"):
        """
        获取当前日期，格式：年月日
        :param formatstr: 时间格式
        :return: 返回当前日期
        """
        a = self.getnowstamp()
        b = self.timechange(a)
        c = time.strftime(formatstr, b)
        return c


if __name__ == '__main__':
    # dt = "2016-05-05 20:28:54"
    t = TimeOperation()
    a = t.getnowstamp()
    print(a)
