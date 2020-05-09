from pyquery import PyQuery as pq

import logging

logger = logging.getLogger('AutoTest')


class GetDocsInfoForUrl:
    """
    @Author: 朱孟彤
    @desc: 接口文档解析封装方法
    """

    def getDocsInfo(self, url):
        """
        通过url解析接口文档
        :param url: 接口文档首页地址
        :return: 解析后的接口文档数据
        """

        logger.info("开始通过url，进行接口文档解析")

        pass_num = 0
        false_num = 0
        false_info = []
        null_num = 0
        null_info = []

        try:
            url_text = pq(url, encoding='utf-8', parser="html")

            url_text = url_text('body')

            # 侧边栏查找菜单按照模块获取数据
            logger.info("获取模块列表")
            model_ele = url_text('.menu ul h2').items()

            model_list = []  # 模块列表

            model_info = {}

            logger.info("循环模块列表，解析每个模块中的接口")
            # 循环每一个模块，获取模块中的内容
            for model in model_ele:
                model_title = model.text()
                model_list.append(model_title)  # 模块名称
                logger.info("开始解析%s模块" + model_title)
                # 获取模块中的内容
                menu_html = model.parent().items()
                # 储存url地址下的所有接口文档信息
                docs_info = []
                logger.info("循环获取每个模块中的接口详情地址，并获取相应的接口数据")
                for menu in menu_html:
                    nav_list = menu('h3')('a').items()
                    for m in nav_list:
                        re_name = m.text()[:-3]  # 接口名称
                        re_path = m.attr.href  # 接口详情地址
                        logger.info("接口文档名称：%s，接口文档详情地址：%s"%(re_name, re_path))
                        re_result = self.getRequestInfo(re_path)
                        if re_result['status'] == 110:
                            # 接口文档详情解析失败
                            false_num += 1
                            false_info.append({'errorPath':re_result['errorPath'],'errorMsg': re_result['errorMsg']})
                            continue
                            # return {'status': 110, 'errorMsg': '解析接口文档地址错误'}
                        elif re_result['status'] == 30:
                            # 接口文档详情页面为空
                            null_num += 1
                            null_info.append(re_result['data'])
                            continue
                        else:
                            docs_info.append(re_result['data'])
                            pass_num += 1
                        logger.info("接口详情地址解析完毕")
                        # logger.info("接口详情地址：%s，解析完毕的信息为：%s"%(re_name, str(request_info)))
                model_info[model_title] = docs_info
                logger.info("所有地址解析完毕")
            exe_info = {
                'pass_num': pass_num,
                'false_num': false_num,
                'false_info': false_info,
                'null_num': null_num,
                'null_info': null_info
                }
            # logger.info("所有地址解析完毕，信息为：" + str(docs_info))
        except Exception as ex:
            return {'status': 110, 'errorMsg': '解析接口文档地址错误，' + str(ex)}
        else:
            return {'status': 20, 'message': '解析接口文档地址成功', 'data': model_info, 'exe_info': exe_info}

    def getRequestInfo(self, re_path):
        """
        根据接口详情的url解析详情页内容
        :param re_path: 接口详情页地址
        :return: 返回接口详情页内容
        """

        logger.info("开始根据url解析接口详情页内容")

        try:

            url_text = pq(re_path, encoding='utf-8', parser="html")

            docs_info = url_text('.markdown-body')

            if not docs_info:

                return {'status': 30, 'message': '接口文档页面内容为空', 'data': re_path}

            request_body = {}

            request_body["docs_path"] = re_path

            request_name = docs_info('h1').text()

            developer_name = docs_info('h1').next().text()

            logger.info("接口名称：%s，开发者：%s"%(request_name, developer_name))

            request_body["RequestName"] = request_name
            request_body["DeveloperName"] = developer_name[4:]

            logger.info("根据模块分区，获取每一个模块的内容")

            for model in docs_info('h2').items():

                # 每个模块的抬头
                model_title = model.text()
                logger.info("当前获取模块为：%s"%model_title)

                next_info = model.next()

                if next_info('p'):
                    # 当内容为文字时，直接用text方法获取文字内容
                    model_info = next_info.text()
                    # model_info = next_info('code').text()
                    logger.info("模块内容为文字，%s"%model_info)
                    request_body[model_title] = model_info

                elif next_info('table'):
                    logger.info("模块内容为表格，开始解析表格")
                    tr_list = []
                    # 获取表头列表
                    logger.info("开始获取表头列表")
                    thead_ele = next_info('table')('tr th').items()
                    th_list = []
                    for thead in thead_ele:
                        th_list.append(thead.text())
                    # 获取表格内容
                    logger.info("开始获取表格内容")
                    tbody_ele = next_info('table')('tbody tr').items()  # 找table的内容，body，根据body寻找tr->td
                    for tbody_info in tbody_ele:
                        td_ele = tbody_info('td').items()  # 获取td集合
                        td_list = []
                        for td in td_ele:
                            td_list.append(td.text())
                            # 循环每一层的td，获取内容
                        tr_list.append(td_list)
                    if tr_list:
                        logger.info("获取内容成功，内容为：%s"%str(tr_list))
                        request_body[model_title] = {"th": th_list, "td": tr_list}
                    else:
                        logger.info("表格无数据")
                        request_body[model_title] = "无"

                elif next_info('code'):
                    logger.info("模块内容为Json示例，直接定位获取")
                    model_info = next_info('code').text()
                    logger.info("示例文字：" + model_info)
                    request_body[model_title] = model_info

            for model in docs_info('h3').items():

                # 每个模块的抬头
                model_title = model.text()
                logger.info("当前获取模块为：%s"%model_title)

                next_info = model.next()

                if next_info('p'):
                    # 当内容为文字时，直接用text方法获取文字内容
                    model_info = next_info.text()
                    # model_info = next_info('code').text()
                    logger.info("模块内容为文字，%s"%model_info)
                    request_body[model_title] = model_info

                elif next_info('table'):
                    logger.info("模块内容为表格，开始解析表格")
                    tr_list = []
                    # 获取表头列表
                    logger.info("开始获取表头列表")
                    thead_ele = next_info('table')('tr th').items()
                    th_list = []
                    for thead in thead_ele:
                        th_list.append(thead.text())
                    # 获取表格内容
                    logger.info("开始获取表格内容")
                    tbody_ele = next_info('table')('tbody tr').items()  # 找table的内容，body，根据body寻找tr->td
                    for tbody_info in tbody_ele:
                        td_ele = tbody_info('td').items()  # 获取td集合
                        td_list = []
                        for td in td_ele:
                            td_list.append(td.text())
                            # 循环每一层的td，获取内容
                        tr_list.append(td_list)
                    if tr_list:
                        logger.info("获取内容成功，内容为：%s"%str(tr_list))
                        request_body[model_title] = {"th": th_list, "td": tr_list}
                    else:
                        logger.info("表格无数据")
                        request_body[model_title] = "无"

                elif next_info('code'):
                    logger.info("模块内容为Json示例，直接定位获取")
                    model_info = next_info('code').text()
                    logger.info("示例文字：" + model_info)
                    request_body[model_title] = model_info

            for model in docs_info('h4').items():

                # 每个模块的抬头
                model_title = model.text()
                logger.info("当前获取模块为：%s"%model_title)

                next_info = model.next()

                if next_info('p'):
                    # 当内容为文字时，直接用text方法获取文字内容
                    model_info = next_info.text()
                    # model_info = next_info('code').text()
                    logger.info("模块内容为文字，%s"%model_info)
                    request_body[model_title] = model_info

                elif next_info('table'):
                    logger.info("模块内容为表格，开始解析表格")
                    tr_list = []
                    # 获取表头列表
                    logger.info("开始获取表头列表")
                    thead_ele = next_info('table')('tr th').items()
                    th_list = []
                    for thead in thead_ele:
                        th_list.append(thead.text())
                    # 获取表格内容
                    logger.info("开始获取表格内容")
                    tbody_ele = next_info('table')('tbody tr').items()  # 找table的内容，body，根据body寻找tr->td
                    for tbody_info in tbody_ele:
                        td_ele = tbody_info('td').items()  # 获取td集合
                        td_list = []
                        for td in td_ele:
                            td_list.append(td.text())
                            # 循环每一层的td，获取内容
                        tr_list.append(td_list)
                    if tr_list:
                        logger.info("获取内容成功，内容为：%s"% str(tr_list))
                        request_body[model_title] = {"th": th_list, "td": tr_list}
                    else:
                        logger.info("表格无数据")
                        request_body[model_title] = "无"

                elif next_info('code'):
                    logger.info("模块内容为Json示例，直接定位获取")
                    model_info = next_info('code').text()
                    logger.info("示例文字：" + model_info)
                    request_body[model_title] = model_info
        except Exception as ex:
            return {'status': 110, 'errorMsg': '接口详情解析失败，' + str(ex), 'errorPath': re_path}
        else:
            return {'status': 20, 'message': '接口详情解析成功', 'data': request_body}


if __name__ == '__main__':
    docs_path = "http://console-api-dev.crs.dev-test.vchangyi.com/doc/index"
    info = GetDocsInfoForUrl()
    print(info.getDocsInfo(docs_path))
