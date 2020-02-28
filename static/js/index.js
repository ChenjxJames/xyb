$(document).ready(function () {
    let isLogin = false;  //前端记录登录状态，减轻后端登录验证模块压力

    //请求服务器更新登陆状态
    $.get("/user/islogin", function (data) {
        isLogin = data.isLogin === "false" ? false : true;
        if (isLogin){
            $("#icon_logout").show();
        }
    });

    queryTaskInfo('');

    //新建任务模态框中的可见选择按钮单击
    $("#btn_visible").click(function () {
        $("#visible_list").show();
    });

    //在导航栏搜索框激活时按下键盘按键
    $("#research_keyword").keydown(function (event) {
        //按下的按键是回车键
        if (event.which === 13) {
            queryTaskInfo($("#research_keyword").val());
        }
    });

    $("#task_list").on("click",".task-", function () {
        if (isLogin){
            window.location.href = "/task_info?task_id="+$(this).attr('task_id');
        } else {
            $("#login").show();
        }

    });

    function queryTaskInfo(keyword) {
        $.getJSON("/query_tasks", {keyword: keyword}, function (data) {
            $("#task_list").empty();
            if (data[0].state === '0') {
                $.each(data[1], function (i, item) {
                    let visible = '';
                    if (item.task_sex_preference === 1) {
                        visible = '-male';
                    } else if (item.task_sex_preference === 2) {
                        visible = '-female';
                    }

                    //合成每个任务的html
                    let html = "<div class='task"+visible+"' onclick='window.location.href=\"/task_info?task_id="+item.task_id+"\"'>\n" +
                            "       <div class='task"+visible+"-content'>\n" +
                            "           <div class='time'>"+item.deadline+"</div>\n" +
                            "           <div class='title'>"+item.task_title+"</div>\n" +
                            "           <div class='money'>￥"+item.task_price+"</div>\n" +
                            "       </div>\n" +
                            "       <div class='icon'>\n" +
                            "           <img src='/static/img/right-arr.png'>\n" +
                            "       </div>\n" +
                            "</div>"
                    $("#task_list").append(html);
                });
            } else {
                alert(data[0].info + '   [' + data[0].state + ']');
            }
        });
    }
});