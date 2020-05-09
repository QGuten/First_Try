#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 2019/5/16
# @Author  : Kris
# @FileName : RandomForToken.py
# @desc     : 随机生成token
import random


def GetCode(n=6, alpha=True):
    """
    @Author: 朱孟彤
    @desc: 生成验证码方法
    :param n: 验证码位数，默认6位
    :param alpha: 验证码类型，True为数字字母混合验证码，False为纯数字验证码，默认为数字字母混合验证码
    :return: 返回生成的验证码
    """
    s = '' # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(0,9)  # 生成随机数字0-9
        if alpha:   # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65,90))
            lower_alpha = chr(random.randint(97,122))
            num = random.choice([num,upper_alpha,lower_alpha])
        s = s + str(num)
    return s
