function signOut(url) {
    //退出登录接口
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: url,//url
        data: '',
        cache: false,
        async: false,
        statusCode: {
            200: function (result) {
                alert(result.data);
                window.location.href = "/login/";
            },
            400: function (result) {
                alert(result.errMsg);
            }
        }
    });
}

//获取table对象，并组成json
function GetTableParams(id) {
    var tb = document.getElementById(id);    //获取table对像
    var rows = tb.rows;
    var cellArr = {};
    for (var i = 1; i < rows.length; i++) {    //--循环所有的行
        var cells = rows[i].cells;
        var key = cells[0].getElementsByTagName("input")[0].value;
        var value = cells[1].getElementsByTagName("input")[0].value;
        if (key != "" && value != "") {
            cellArr[key] = value;
        }
    }
    var result_info = JSON.stringify(cellArr);
    return result_info
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

jQuery.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            xhr.setRequestHeader("Content-Type", "application/json");
        }
    }
});
