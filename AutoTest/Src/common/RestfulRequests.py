# coding:utf-8
import json
import requests


def send_restFul(data):
    """
    @Author: 朱孟彤
    @desc: 发送restful接口方法

    :param data: 接口发送信息
    :return: 返回发送结果
    """
    method = data["method"]  # post or get
    url = data["url"]
    # url后面的params参数
    try:
        params = data["params"]
    except:
        params = None
    # 请求头部headers
    try:
        headers = data["headers"]
    except:
        headers = None
    # post请求body类型
    type = data["type"]   # json or data
    # post请求body内容
    try:
        bodydata = eval(data["body"])
    except:
        bodydata = {}
    # 判断传data数据还是json
    if type == "data":
        body = bodydata
    elif type == "json":
        body = json.dumps(bodydata)
    else:
        body = bodydata
    res = {}  # 接受返回数据
    try:
        r = requests.request(
                      method=method,
                      url=url,
                      params=params,
                      headers=headers,
                      data=body,
                      verify=False,
                       )
        print("页面返回信息：%s" % r.content.decode("utf-8"))
        res["statuscode"] = str(r.status_code)  # 状态码转成str
        res["text"] = r.content.decode("utf-8")
        res["times"] = str(r.elapsed.total_seconds())   # 接口请求时间转str
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        return res
    except Exception as msg:
        res["msg"] = str(msg)
        return res