from django import template
from ast import literal_eval

register = template.Library()


@register.inclusion_tag("layout/_left_nav.html")  # django会自动去templates中寻找
def get_menu_styles(request):
    """
    @Author: 朱孟彤
    @desc: 加载获取的权限菜单列表
    :param request: request对象
    :return: 返回权限菜单列表
    """
    permission_menu_dict = request.session.get("permission_menu_dict")
    return {"permission_menu_dict": permission_menu_dict}


@register.simple_tag
def data_table(data):
    """
    @Author: 朱孟彤
    @desc: 接口详情页，数据处理成表格的过滤器
    :param data:需要转换的数据
    :return:转换后的HTML数据
    """
    # print(data)
    # print(type(data))
    if data:
        if data != '无' and data != '{}':
            data = eval(data)
            if isinstance(data, str):
                html = '<input type="text" name="password" placeholder="'+data+'" autocomplete="off" class="layui-input" disabled>'
                return html
            elif isinstance(data, dict):
                # 判断数据是单一表格，还是大字典中嵌套
                if data.__contains__('th'):
                    html = '<table class="layui-table"><thead><tr>'
                    # 解析表头
                    th_list = data['th']
                    for th in th_list:
                        html += '<th>'+th+'</th>'
                    html += '</tr></thead><tbody>'
                    # 开始表格数据
                    tr_list = data['td']
                    for tr in tr_list:
                        if tr != '':
                            html += '<tr>'
                            for td in tr:
                                # if td == '':
                                #     html = '<input type="text" name="password" placeholder="无" autocomplete="off" class="layui-input" disabled>'
                                #     print(html)
                                #     return html
                                # else:
                                #     html += '<td>' + td + '</td>'
                                html += '<td>' + td + '</td>'
                            html += '<tr>'
                    html += '</tbody></table>'
                    return html
                else:
                    html = ''
                    for key in data.keys():
                        table_info = data[key]
                        html += '<fieldset class="layui-elem-field layui-field-title"><legend>'+key+'</legend>'

                        html += '<div class="layui-field-box"><table class="layui-table"><thead><tr>'
                        # 解析表头
                        th_list = table_info['th']
                        for th in th_list:
                            html += '<th>' + th + '</th>'
                        html += '</tr></thead><tbody>'
                        # 开始表格数据
                        tr_list = table_info['td']
                        for tr in tr_list:
                            if tr != '':
                                html += '<tr>'
                                for td in tr:
                                    if td == '':
                                        html = '<input type="text" name="password" placeholder="无" autocomplete="off" class="layui-input" disabled>'
                                        return html
                                    else:
                                        html += '<td>' + td + '</td>'
                                html += '<tr>'
                        html += '</tbody></table></div></fieldset>'
                    return html
            else:
                html = '<input type="text" name="password" placeholder="'+data+'" autocomplete="off" class="layui-input" disabled>'
            return html
        else:
            html = '<input type="text" name="password" placeholder="' + data + '" autocomplete="off" class="layui-input" disabled>'
            return html
    else:
        html = '<input type="text" name="password" placeholder="无" autocomplete="off" class="layui-input" disabled>'
        return html


@register.simple_tag
def execute_info_table(data):
    """
    @Author: 朱孟彤
    @desc: 测试用例执行参数，转化为表格过滤器
    :param data:需要转换的数据
    :return:转换后的HTML数据
    """
    if data:
        # print(data)
        if data != '无' and data != '[]':
            data = eval(data)
            if isinstance(data, list):
                html = '<table class="layui-table"><thead><tr><th>字段名</th><th>类型</th><th>是否必填</th><th>值</th><th>描述</th></tr></thead><tbody>'
                for d in data:
                    # d = eval(d)
                    html += '<tr>'
                    html += '<td>' + d['name'] + '</td>'
                    html += '<td>' + d['type'] + '</td>'
                    html += '<td>' + d['if_must'] + '</td>'
                    if d.__contains__('value'):
                        html += '<td>' + d['value'] + '</td>'
                    else:
                        html += '<td></td>'
                    html += '<td>' + d['des'] + '</td>'
                    html += '</tr>'
                html += '</tbody></table>'
                return html
            elif isinstance(data, dict):
                html = '<table class="layui-table"><thead><tr><th>字段名</th><th>类型</th><th>是否必填</th><th>值</th><th>描述</th></tr></thead><tbody>'
                # d = eval(d)
                html += '<tr>'
                html += '<td>' + data['name'] + '</td>'
                html += '<td>' + data['type'] + '</td>'
                html += '<td>' + data['if_must'] + '</td>'
                if data.__contains__('value'):
                    html += '<td>' + data['value'] + '</td>'
                else:
                    html += '<td></td>'
                html += '<td>' + data['des'] + '</td>'
                html += '</tr>'
                html += '</tbody></table>'
                return html
            elif isinstance(data, str):
                html = '<input type="text" name="password" placeholder="'+data+'" autocomplete="off" class="layui-input" disabled>'
                return html
        elif isinstance(data, str):
            html = '<input type="text" name="password" placeholder="' + data + '" autocomplete="off" class="layui-input" disabled>'
            return html
    elif isinstance(data, str):
        html = '<input type="text" name="password" placeholder="' + '无' + '" autocomplete="off" class="layui-input" disabled>'
        return html


@register.simple_tag
def param_info_table(data):
    """
    @Author: 朱孟彤
    @desc: 测试用例预期参数，转化为表格过滤器
    :param data: 需要转换的数据
    :return: 转换后的HTML数据
    """
    if data:
        # print(data)
        if data != '无' and data != '[]':
            data = eval(data)
            if isinstance(data, list):
                html = '<table class="layui-table"><thead><tr><th>字段名</th><th>类型</th><th>是否必填</th><th>值</th><th>描述</th></tr></thead><tbody>'
                for d in data:
                    # d = eval(d)
                    html += '<tr>'
                    html += '<td>' + d['name'] + '</td>'
                    html += '<td>' + d['type'] + '</td>'
                    html += '<td>' + d['if_must'] + '</td>'
                    if d.__contains__('value'):
                        html += '<td>' + d['value'] + '</td>'
                    else:
                        html += '<td></td>'
                    html += '<td>' + d['des'] + '</td>'
                    html += '</tr>'
                html += '</tbody></table>'
                return html
            elif isinstance(data, dict):
                html = '<table class="layui-table"><thead><tr><th>字段名</th><th>类型</th><th>是否必填</th><th>值</th><th>描述</th></tr></thead><tbody>'
                # d = eval(d)
                html += '<tr>'
                html += '<td>' + data['name'] + '</td>'
                html += '<td>' + data['type'] + '</td>'
                html += '<td>' + data['if_must'] + '</td>'
                if data.__contains__('value'):
                    html += '<td>' + data['value'] + '</td>'
                else:
                    html += '<td></td>'
                html += '<td>' + data['des'] + '</td>'
                html += '</tr>'
                html += '</tbody></table>'
                return html
            elif isinstance(data, str):
                html = '<input type="text" name="password" placeholder="'+data+'" autocomplete="off" class="layui-input" disabled>'
                return html
        elif isinstance(data, str):
            html = '<input type="text" name="password" placeholder="' + data + '" autocomplete="off" class="layui-input" disabled>'
            return html
    elif isinstance(data, str):
        html = '<input type="text" name="password" placeholder="' + '无' + '" autocomplete="off" class="layui-input" disabled>'
        return html


@register.simple_tag
def show_job_record_info(data):
    """
    @Author: 朱孟彤
    @desc: 任务执行详细页面，任务执行记录信息数据处理成表格的过滤器
    :param data: data 任务执行记录的信息，需要转换的数据
    :return: 转换后的HTML数据
    """
    data = eval(data)
    # print(data)
    if data:
        html = '<div class="layui-collapse lay-accordion">'
        for i in data:
            html += '<div class="layui-colla-item">'
            html += '<h2 class="layui-colla-title">执行详情</h2>'
            html += '<div class="layui-colla-content layui-show">'
            html += '<form class="layui-form">'

            html += '<div class="layui-form-item">'
            html += '<label class="layui-form-label">通过数量</label>'
            html += '<div class="layui-input-inline">'
            html += '<input type="text" name="re_id" id="suite_id" placeholder="' + str(i["pass_num"]) + '" autocomplete="off" class="layui-input" disabled>'
            html += '</div></div>'

            html += '<div class="layui-form-item">'
            html += '<label class="layui-form-label">失败数量</label>'
            html += '<div class="layui-input-inline">'
            html += '<input type="text" name="re_id" id="suite_id" placeholder="' + str(i["false_num"]) + '" autocomplete="off" class="layui-input" disabled>'
            html += '</div></div>'

            html += '<div class="layui-form-item">'
            html += '<label class="layui-form-label">失败详情</label>'
            html += '<div class="layui-input-block">'
            html += '<input type="text" name="re_id" id="suite_id" placeholder="' + str(i["false_info"]) + '" autocomplete="off" class="layui-input" disabled>'
            html += '</div></div>'

            html += '<div class="layui-form-item">'
            html += '<label class="layui-form-label">为空数量</label>'
            html += '<div class="layui-input-inline">'
            html += '<input type="text" name="re_id" id="suite_id" placeholder="' + str(i["null_num"]) + '" autocomplete="off" class="layui-input" disabled>'
            html += '</div></div>'

            html += '<div class="layui-form-item">'
            html += '<label class="layui-form-label">为空详情</label>'
            html += '<div class="layui-input-block">'
            html += '<input type="text" name="re_id" id="suite_id" placeholder="' + str(i["null_info"]) + '" autocomplete="off" class="layui-input" disabled>'
            html += '</div></div>'

            html += '</form></div></div>'
            html += ''
            html += ''
        html += '</div>'
        return html
    else:
        html = ''
        return html


@register.simple_tag
def job_header_to_table(data):
    """
    @Author: 朱孟彤
    @desc: 任务详情页面，任务请求头转换html
    :param data: data 需要转换的数据
    :return: 转换后的HTML数据
    """
    if data:
        data = eval(data)
        if len(data) != 0:
            html = '<table class="layui-table"><thead><tr><th>参数名</th><th>参数值</th></tr></thead><tbody>'
            for info in data:
                for key, value in info.items():
                    # print(key, value)
                    html += '<tr>'
                    html += '<td>'
                    html += key
                    html += '</td>'
                    html += '<td>'
                    html += value
                    html += '</td>'
                    html += '</tr>'
            html += '</tbody></table>'
            return html
        else:
            html = '<input type="text" name="password" placeholder="无" autocomplete="off" class="layui-input" disabled>'
            return html
    else:
        html = '<input type="text" name="password" placeholder="无" autocomplete="off" class="layui-input" disabled>'
        return html


@register.simple_tag
def job_data_to_table(data):
    """
    @Author: 朱孟彤
    @desc: 任务详情页面，任务执行数据转换html
    :param data: data 需要转换的数据
    :return: 转换后的HTML数据
    [{"step_id":"377","data":"{\"exe_params\":{\"qy_domain\":\"2\",\"condition\":\"3\"},\"result\":{\"status\":\"4\"}}"}]
    """
    # print(data)
    # print(type(data))
    data = eval(data)
    if data:
        if isinstance(data, list):
            for info in data:
                # 步骤顺序
                html = '<hr class="layui-bg-green">'
                html += '<div class="step_info">'
                html += '<div class="layui-form-item">'
                html += '<label class="layui-form-label">步骤ID</label>'
                html += '<div class="layui-input-block">'
                html += '<input type="text" name="step_id" id="step_id" placeholder="' + str(info["step_id"]) + '" autocomplete="off" class="layui-input" disabled>'
                html += '</div></div>'

                exe_data = eval(info["data"])

                exe_params = exe_data["exe_params"]
                # print(exe_params)

                html += '<div class="layui-form-item">'
                html += '<label class="layui-form-label">请求数据</label>'
                html += '<div class="layui-input-block">'

                html += '<table class="layui-table" id="params_table"><thead><tr><th>参数名</th><th>请求值</th></tr></thead><tbody>'
                for key, value in exe_params.items():
                    # print(key, value)
                    html += '<tr>'
                    html += '<td>'
                    # html += '<input type="text" value="' + key + '" autocomplete="off" class="layui-input" disabled>'
                    html += '<input type="text" value="' + key + '" autocomplete="off" class="layui-input">'
                    html += '</td>'
                    html += '<td>'
                    html += '<input type="text" value="' + value + '" autocomplete="off" class="layui-input">'
                    html += '</td>'
                    html += '</tr>'

                html += '</tbody></table>'
                html += '</div></div>'

                result_params = exe_data["result"]
                # print(result_params)

                html += '<div class="layui-form-item">'
                html += '<label class="layui-form-label">断言数据</label>'
                html += '<div class="layui-input-block">'

                html += '<table class="layui-table" id="result_table"><thead><tr><th>参数名</th><th>请求值</th></tr></thead><tbody>'
                for key, value in result_params.items():
                    # print(key, value)
                    html += '<tr>'
                    html += '<td>'
                    # html += '<input type="text" value="' + key + '" autocomplete="off" class="layui-input" disabled>'
                    html += '<input type="text" value="' + key + '" autocomplete="off" class="layui-input">'
                    html += '</td>'
                    html += '<td>'
                    html += '<input type="text" value="' + value + '" autocomplete="off" class="layui-input">'
                    html += '</td>'
                    html += '</tr>'

                html += '</tbody></table>'
                html += '</div></div>'

                html += '<div class="layui-form-item">'
                html += '<label class="layui-form-label">储存参数</label>'
                html += '<div class="layui-input-block">'

                if exe_data.__contains__('save_list'):
                    save_list = exe_data["save_list"]
                    html += '<input type="text" name="save_list" id="save_list" value="'+str(save_list)+'" autocomplete="off" class="layui-input">'
                else:
                    html += '<input type="text" name="save_list" id="save_list" autocomplete="off" class="layui-input">'

                html += '</div></div>'
                html += '<div class="layui-form-item">'
                html += '<div class="layui-input-block">'
                html += '<div class="layui-form-mid layui-word-aux">'
                html += '请输入该用例步骤执行后需要储存的参数列表，多参数用;分隔开，若储存时，需要更改参数名，请用:更改后的参数名。例如：a:b;c'
                html += '</div>'
                html += '</div>'
                html += '</div>'

                html += '</div>'

                return html
        else:
            html = ''
            return html
    else:
        html = ''
        return html


@register.simple_tag
def count_info(data):
    """
    @Author: 朱孟彤
    @desc: 测试报告展示，把json对象，转换为文字展示
    :param data: 需要转换的数据
    :return: 转换后的HTML数据
    {'case_count': 1, 'case_succeed': 1, 'case_fail': 0}
    """
    if data:

        data = literal_eval(data)

        return_data = ''

        if isinstance(data, dict):
            for key in data.keys():
                if "all" in key:
                    return_data += '共计数量：' + str(data[key]) + '\n'
                elif "pass" in key:
                    return_data += '执行成功数量：' + str(data[key]) + '\n'
                elif "fail" in key:
                    return_data += '执行失败数量：' + str(data[key]) + '\n'

        return return_data

    elif isinstance(data, str):

        return ''
