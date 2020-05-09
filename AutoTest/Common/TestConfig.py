# -*- coding: utf-8 -*-
# @Time    : 2018/09/29 17:00
# @Author  : 朱孟彤
# @File    : TestConfig.py
# @desc:ini文件、excel文件读取类
import os
import configparser
import xlrd


class IniOperation:
    """
    @Author: 朱孟彤
    @desc: ini配置文件操作类
    """

    def __init__(self):
        self.conf = configparser.ConfigParser()

    @classmethod
    def GetIniPath(self, ininame):
        '''获取ini文件目录'''
        try:
            p = os.path.dirname(os.path.realpath(__file__))
            p = os.path.dirname(p)
            file_path = os.path.join(p, "config", ininame)
        except Exception as pe:
            print("Get path error:%s" % pe)
        else:
            return file_path

    def OpenIni(self, file_path):
        '''读取ini文件'''
        try:
            self.conf.read(file_path)
        except Exception as oe:
            print("Open ini error:%s" % oe)

    def GetSection(self):
        '''获取所有的section'''
        try:
            sections = self.conf.sections()
        except Exception as gs:
            print("Get section error:%s" % gs)
        else:
            return sections

    def GetOption(self, section, value, type):
        '''获取指定的section，指定的option的值'''
        try:
            if type == "str":
                value = self.conf.get(section, value)
            elif type == "int":
                value = self.conf.getint(section, value)
        except Exception as ve:
            print("Get option error:%s" % ve)
        else:
            return value

    def NewOption(self, section, option, value):
        '''更新指定section, option的值（包含添加）'''
        try:
            self.conf.set(section, option, value)
        except Exception as ne:
            print("Update option error:%s" % ne)

    def AddSection(self, new_section):
        '''添加新的section'''
        try:
            self.conf.add_section(new_section)
        except Exception as ae:
            print("Add new section error:%s" % ae)

    def WriteIni(self, path):
        '''写回配置文件'''
        try:
            self.conf.write(open(path, "w"))
        except Exception as we:
            print("Write ini error:%s" % we)

    def GetOptions(self, section):
        '''获取section下的options，返回list'''
        try:
            oplist = self.conf.options(section)
        except Exception as oe:
            print("Get options for section error:%s" % oe)
        else:
            return oplist

    def GetAllKeys(self, section):
        '''获取section下的键对值，返回list，list中的元素为元组'''
        try:
            oplist = self.conf.items(section)
        except Exception as oe:
            print("Get options for section error:%s" % oe)
        else:
            return oplist

    def RemoveSection(self, section):
        '''删除section'''
        try:
            self.conf.remove_section(section)
        except Exception as re:
            print("Remove section error:%s" % re)

    def RemoveOption(self, section, option):
        '''删除指定section下的option'''
        try:
            self.conf.remove_option(section, option)
        except Exception as re:
            print("Remove option error:%s" % re)


class XlsxOperation():
    """
    @Author: 朱孟彤
    @desc: 配置文件读取、操作
    """

    def OpenXlsx(self, xlsxname):
        '''打开xlsx文件，返回文件内容'''
        try:
            path = os.path.realpath(__file__)
            path = os.path.join(os.path.dirname(path), xlsxname)
            bk = xlrd.open_workbook(path)
        except Exception as oe:
            print("Open xlsx error:%s" % oe)
        else:
            return bk

    def ReturnXlsxSheet(self, bk):
        '''获取文档中所有的sheet名称'''
        try:
            sheetname = bk.sheet_names()
        except Exception as se:
            print("Xlex sheet get error:%s" % se)
        else:
            return sheetname

    def GetXlsxText(self, by, text, xlsxtest):
        '''根据index获取xlsx中的内容，返回当前sheet中的内容'''
        if by == "index":
            table = xlsxtest.sheet_by_index(text)
        elif by == "name":
            table = xlsxtest.sheet_by_name(text)
        else:
            table = xlsxtest.sheets()[text]
        return table

    def ReturnXlsxRows(self, table):
        '''读取行数，返回行数'''
        try:
            nrows = table.nrows
        except Exception as re:
            print("Get sheet rows error:%s" % re)
        else:
            return nrows

    def ReturnXlsxCols(self, table):
        '''读取列数，返回列数'''
        try:
            nrows = table.ncols
        except Exception as ce:
            print("Get sheet cols error:%s" % ce)
        else:
            return nrows

    def ReturnXlsxName(self, table):
        '''读取sheet名称，返回列数'''
        try:
            sheetname = table.name
        except Exception as ne:
            print("Get sheet name error:%s" % ne)
        else:
            return sheetname

    def GetRowsText(self, table, num):
        '''获取整行的内容，返回值list'''
        try:
            rowstext = table.row_values(num)
        except Exception as te:
            print("Get row text error:%s" % te)
        else:
            return rowstext

    def GetColsText(self, table, num):
        '''获取整列的内容，返回值list'''
        try:
            clostext = table.col_values(num)
        except Exception as le:
            print("Get los text error:%s" % le)
        else:
            return clostext

    def GetCols(self, table, mun):
        '''以行为准输出每行的内容,mun是列'''
        try:
            for i in range(0, mun):
                b = self.GetRowsText(table, i)
                for j in b:
                    print(j),
                print()
        except Exception as ce:
            print("Print text error for cols:%s" % ce)

    def GetRows(self, table, num):
        '''以列为准输出每列的内容，num是行'''
        try:
            for n in range(0, num):
                p = self.GetColsText(table, n)
                for m in p:
                    print(m),
                print()
        except Exception as re:
            print("Print text error for rows:%s" % re)
