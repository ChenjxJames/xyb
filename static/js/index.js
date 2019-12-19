$(document).ready(function () {
    let count = 1;        //验证码计算器
    let isLogin = false;  //前端记录登录状态，减轻后端登录验证模块压力
    let sex = '0';      //发布任务性别限定（0:all, 1:man, 2:woman）

    //请求服务器更新登陆状态
    $.get("/user/islogin", function (data) {
        isLogin = data.isLogin === "false" ? false : true;
        if (isLogin){
            $("#icon_logout").show();
        }
    });

    set_xy();
    // 当窗体大小改变时调节photo-slide高度
    $(window).resize(function () {
        set_xy();
    });

    queryTaskInfo('');

    //打开新建任务模态框
    $("#btn_add_task").click(function () {
        if (isLogin) {
            $("#modal_add_task").show();
        } else {
            $("#login").show();
        }
    });

    //点击关闭新建任务模态框
    $("#modal_add_task_curtain").click(function () {
        $("#modal_add_task").hide();
    });

    //点击按钮关闭新建任务模态框
    $("#add_close").click(function () {
        $("#modal_add_task").hide();
    });

    //关闭登录模态框
    $("#login_curtain").click(function () {
        $("#login").hide();
    });

    //打开登录模态框
    $("#icon_personal").click(function () {
        if (isLogin) {
            window.location.pathname = '/user/user_info';
        } else {
            $("#login").show();
        }
    });

    $(window).scroll(function () {
        if ($(window).scrollLeft() > 0) {
            $("nav").css("margin-left", -$(window).scrollLeft());
        }

        if ($(window).scrollTop() > $(".roll-giant-img").height() + 60) {
            $("#tool").addClass("content-tool-hang");
            $("#nav_research").show();
            $("#roll_giant_research").hide();
        } else {
            $("#tool").removeClass("content-tool-hang");
            $("#nav_research").hide();
            $("#roll_giant_research").show();
        }
    });

    //当输入密码后，加载图片验证码
    $("#user_psd").blur(function () {
        $("#identity").show();
        refreshIdentifyCode();
    });

    //点击图片验证码，切换验证码
    $("#identity").click(function () {
        refreshIdentifyCode();
    });

    //登录按钮点击
    $("#btn_login").click(function () {
        if (isValid()) {
            loginAjax();
        }
    });

    //在登录激活时按下键盘按键
    $("#login").keydown(function (event) {
        //按下的按键是回车键
        if (event.which === 13) {
            if (isValid()) {
                loginAjax();
            }
        }
    });

    //新建任务模态框中的可见选择按钮单击
    $("#btn_visible").click(function () {
        $("#visible_list").show();
    });

    //设置为全部人可见
    $("#visible_all").click(function () {
        $("#btn_visible").text("全部");
        $("#visible_list").hide();
        sex = 0;
    });

    //设置为仅女生可见
    $("#visible_female").click(function () {
        $("#btn_visible").text("仅女生可见");
        $("#visible_list").hide();
        sex = 2;
    });

    //设置为仅男生可见
    $("#visible_male").click(function () {
        $("#btn_visible").text("仅男生可见");
        $("#visible_list").hide();
        sex = 1;
    });

    //发布任务按钮单击
    $("#btn_add_task_submit").click(function () {
        if (createTaskIsValid()) {
            createTaskAjax();
        }
    });

    //两个搜索框联动
    $("#research_keyword").change(function () {
        $("#research_keyword_gaint").val($("#research_keyword").val());
    });

    //两个搜索框联动
    $("#research_keyword_gaint").change(function () {
        $("#research_keyword").val($("#research_keyword_gaint").val());
    });

    //导航栏搜索框搜索
    $("#btn_research").click(function () {
        queryTaskInfo($("#research_keyword").val());
    });

    //大图搜索框搜索
    $("#research_keyword_gaint").click(function () {
        queryTaskInfo($("#research_keyword_gaint").val());
    });

    //在导航栏搜索框激活时按下键盘按键
    $("#research_keyword").keydown(function (event) {
        //按下的按键是回车键
        if (event.which === 13) {
            queryTaskInfo($("#research_keyword").val());
        }
    });

    //在大图搜索框激活时按下键盘按键
    $("#research_keyword_gaint").keydown(function (event) {
        //按下的按键是回车键
        if (event.which === 13) {
            queryTaskInfo($("#research_keyword_gaint").val());
        }
    });

    //推荐任务栏
    $("#divide-sug").click(function () {
        $("#divide-sug").addClass('divide-option');
        $("#divide-col").removeClass('divide-option');
        queryTaskInfo('');
    });

    //关注任务栏
    $("#divide-col").click(function () {
        $("#divide-col").addClass('divide-option');
        $("#divide-sug").removeClass('divide-option');
        $("#task_list").empty();
        $("#task_list").append('<p>您目前还没有关注过其他用户哦！</p>');
    });

    $("#task_list").on("click",".task-", function () {
        if (isLogin){
            window.location.href = "/task_info?task_id="+$(this).attr('task_id');
        } else {
            $("#login").show();
        }

    });

    $("#btn_task_backlog").click(function () {
        window.location.href = "/user/user_info?task=true";
    });

    $("#btn_task_over").click(function () {
        window.location.href = "/user/user_info?task=true";
    });

    function queryTaskInfo(keyword) {
        $.getJSON("/query_tasks", {keyword: keyword}, function (data) {
            $("#task_list").empty();
            if (data[0].state === '0') {
                $.each(data[1], function (i, item) {
                    let imgHtml = '';
                    if (item.task_sex_preference === 0) {
                        imgHtml = '<img src="/static/img/all.png" class="task-icon-item" alt="该任务不限性别" title="该任务不限性别"/>';
                    } else if (item.task_sex_preference === 1) {
                        imgHtml = '<img src="/static/img/man.png" class="task-icon-item" alt="该任务仅限男性" title="该任务仅限男性"/>';
                    } else {
                        imgHtml = '<img src="/static/img/woman.png" class="task-icon-item" alt="该任务仅限女性" title="该任务仅限女性"/>';
                    }

                    //合成每个任务的html
                    let html = '<div class="task-" task_id="' + item.task_id + '" user_id="' + item.user_id + '"><!--单个任务-->\n' +
                        '            <div class="task-title">' + item.task_title + '</div><!--任务标题-->\n' +
                        '            <div class="task-body">\n' +
                        '                <img src="/static/img/task.jpg" class="task-img" alt="任务图片"><!--任务图片-->\n' +
                        '                <div class="task-des">\n' +
                        '                    <div class="task-des-inf">' + item.task_detail + '</div>\n' +
                        '                    <div class="task-icon">\n' +
                        '                        <img src="/static/img/price.png" class="task-icon-item"  title="￥' + item.task_price + '" />\n' +
                        '                        <div class="task-price-text display-inline-block-style">' + item.task_price + '</div>\n' +
                        '                        <img src="/static/img/collect.png" class="task-icon-item"/>\n' + imgHtml +
                        '                    </div><!--图标-->\n' +
                        '                </div><!--任务描述-->\n' +
                        '            </div>\n' +
                        '        </div>';
                    $("#task_list").append(html);
                });
            } else {
                alert(data[0].info + '   [' + data[0].state + ']');
            }
        });
    }


    function loginAjax() {
        $.ajax({
            url: "/user/login",
            data: {
                username: $("#user_name").val(),
                password: $.md5($("#user_psd").val()),
                keep_login: $("input[name='keep_login']:checked").val(),
                identity_code: $("#identify_code").val()
            },
            type: "post",
            dataType: "json",
            async: true,
            success: function (data) {
                if (data.state === '0') {
                    alert("登陆成功！");
                    $("#login").hide();
                    isLogin = true;
                    $("#icon_logout").show();
                } else if (data.state === '-1') {
                    alert("验证码过期或验证码输入错误！");
                    refreshIdentifyCode();
                } else {
                    alert(data.info + '   [' + data.state + ']');
                }
            },
            error: function () {
                alert("ajax error");
            }
        });
    }

    function createTaskAjax() {
        $.ajax({
            url: "/create_task",
            data: {
                title: $("#task_theme").val(),
                detail: $("#task_detail").val(),
                price: $("#task_price").val(),
                sex_preference: sex,
                deadline: $("input.wui-date-input.task-deadtime.div-inline-block").val()
            },
            type: "post",
            dataType: "json",
            async: true,
            success: function (data) {
                if (data.state === '0') {
                    alert("创建任务成功！");
                    $("#research_keyword").val('');
                    $("#research_keyword_gaint").val('');
                    $("#modal_add_task").hide();
                    queryTaskInfo('');
                } else {
                    alert(data.info + '   [' + data.state + ']');
                }
            },
            error: function () {
                alert("ajax error");
            }
        });
    }

    function createTaskIsValid() {
        let title = $("#task_theme");
        let detail = $("#task_detail");
        let price = $("#task_price");
        let deadline = $("input.wui-date-input.task-deadtime.div-inline-block");

        if (title.val().trim().length === 0) {
            title.focus();
            alert("请输入任务标题！");
            return false;
        }
        if (detail.val().trim().length === 0) {
            detail.focus();
            alert("请输入任务详情！");
            return false;
        }
        if (price.val().trim().length === 0) {
            price.focus();
            alert("请输入任务赏金！");
            return false;
        }
        if (deadline.val().trim().length === 0) {
            deadline.focus();
            alert("请输入任务截止时间！");
            return false;
        }
        return true;
    }

    function isValid() {
        let user_name = $("#user_name");
        if (user_name.val().trim().length === 0) {
            user_name.focus();
            alert("请输入您的用户名！");
            return false;
        }
        let user_psd = $("#user_psd");
        if (user_psd.val().trim().length === 0) {
            user_psd.focus();
            alert("请输入您的密码！");
            return false;
        }
        let identify_code = $("#identify_code");
        if (identify_code.val().trim().length === 0) {
            identify_code.focus();
            alert("请输入验证码！");
            return false;
        }
        return true;
    }

    //登录验证码刷新
    function refreshIdentifyCode() {
        count++;
        $("#identity").attr("src", "/user/identify_code?count=" + count);
    }

});

function set_xy() {
    $(".roll-giant").height($(".roll-giant-img").height());
}
