# -*- coding: utf-8 -*-
# @Time    : now()
# @Author  : AngesZhu
# @File    : .py
# @desc:
from kazoo.client import KazooClient
from urllib.parse import unquote


class GetDubboInfoForZK:
    """
    @Author: 朱孟彤
    @desc: python操作zk查询dubbo的基础类
    """

    def createzk(self, host):
        """
        创建一个zk链接
        :return 返回zk链接
        """
        zk = KazooClient(hosts=host)
        zk.start()
        return zk

    def getallinterfaceforaldb(self, zk):
        """
        通过zk链接，查询所有注册包含aldb的interface
        :param zk:
        :return: 返回interface的分类以及列表
        """
        # 查找zk dubbo-online下面的子节点
        children = zk.get_children('/dubbo-online')
        # 筛选出method为空的interface
        c = []
        if isinstance(children, list):
            for inter in children:
                if zk.get_children('/dubbo-online/%s/providers' % inter):
                    c.append(inter)
        # 筛选出包含aldb的interface
        mudel = []
        for i in c:
            # 取出所有模块的名称
            if 'com.aldb.' == i[0:9]:
                s = str(i)
                l = s.split('.')
                mudel.append(l[2])
        m = set(mudel)  # 去重模块名称
        # 生成模块名以及所对应的interface列表的字典
        d = {}
        for n in m:
            o = []
            for j in c:
                if n in j:
                    o.append(j)
            d[n] = o
        return d

    def getinfofrominterface(self, zk, interface):
        """
        根据interface获取信息
        :param zk: zk链接
        :param interface: 要查询的interface
        :return: interface对应的信息
        """
        children = zk.get_children('/dubbo-online/%s/providers' % interface)
        if children:
            info = children[0]
            if isinstance(info, str):
                j = unquote(info)
                l = j.split("&")
                return l

    def infohandle(self, zk, interface):
        """
        根据interface获取信息
        :param zk: zk链接
        :param interface: 要查询的interface
        :return: interface对应的信息
        """
        infodict = {}
        infodict['interface'] = interface
        allinfo = self.getinfofrominterface(zk=zk, interface=interface)
        hosts = allinfo[0]
        hosts = hosts.split("/")[2]  # 字符串截取方式获取ip和端口号
        infodict['hosts'] = hosts
        for i in allinfo:
            if 'methods' in i:
                if isinstance(i, str):
                    l = i.split("=")
                    methods = l[1].split(',')
                    infodict['methods'] = methods
        return infodict


if __name__ == '__main__':
    zktelent = GetDubboInfoForZK()
    zk = zktelent.createzk(host='10.148.16.24:2181')
    print(zktelent.getallinterfaceforaldb(zk))
    # children = zk.get_children('/dubbo-online')
    # print(children)
    # print(type(children))
    # for i in children:
    # 	# print(i)
    # 	info=zk.get_children('/dubbo-online/%s/providers' % i)
    # 	if info:
    # 		info=info[0]
    # 		if isinstance(info, str):
    # 			j = unquote(info)
    # 			l = j.split("&")
    # 			print(l)
    # d = zktelent.getallinterfaceforaldb(zk)
    # info  = zktelent.infohandle(zk,'com.aldb.magiclub.api.facade.CardFacade')
    # print(info)
    # print(info['methods'])
    # m = d.keys()
    # print(list(m).sort())
    zk.stop()
