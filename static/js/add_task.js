$(document).ready(function () {
    let sex = 0;      //发布任务性别限定（0:all, 1:man, 2:woman）
    $("#visible_list").hide();

    if (getUrlParam('task_id')) {
        $.post("/task_info", {task_id: getUrlParam("task_id")}, function f(data) {
            if (data[0].state === '0') {
                $("#task_theme").val(data[1].task_title);
                $("#task_detail").val(data[1].task_detail);
                $("#task_price").val(data[1].task_price);
                $("input.wui-date-input.task-deadtime.div-inline-block").val(data[1].deadline);
                sex = data[1].task_sex_preference;
                if (data[1].task_sex_preference === 0) {
                    $("#set_visible>span").text("公开");
                } else if(data[1].task_sex_preference === 1) {
                    $("#set_visible>span").text("仅男生可领");
                } else if(data[1].task_sex_preference === 2) {
                    $("#set_visible>span").text("仅女生可领");
                }
                let task_can_accept = data[1].task_can_accept;
                if (task_can_accept === '-1') {
                    $(".index-title").text("修改任务信息");
                    $(".index-discrible").text("请详细准确的填写信息。")
                    $("#btn_add_task_submit").hide();
                    $("#btn_set_task").show();
                }
            }
        });
    }
    
    $("#kf").click(function() { 
        alert("客服QQ：1305612581\n客服电话：18324389821"); 
    }); 

    $("body").click(function () {
        $("#visible_list").hide();
    });

    $("#set_visible").click(function (event) {
       $("#visible_list").show();
        event.stopPropagation();
    });

    //设置为全部人可见
    $("#visible_all").click(function () {
        $("#set_visible>span").text("公开");
        sex = 0;
    });

    //设置为仅男生可见
    $("#visible_male").click(function () {
        $("#set_visible>span").text("仅男生可领");
        sex = 1;
    });

    //设置为仅女生可见
    $("#visible_female").click(function () {
        $("#set_visible>span").text("仅女生可领");
        sex = 2;
    });

    //发布任务按钮单击
    $("#btn_add_task_submit").click(function () {
        if (createTaskIsValid()) {
            createTaskAjax("/create_task");
        }
    });

    $("#btn_set_task").click(function () {
        if (createTaskIsValid()) {
            createTaskAjax("/set_task");
        }
    });

    function createTaskAjax(url) {
        $.ajax({
            url: url,
            data: {
                task_id: getUrlParam('task_id'),
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
                    alert(data.info);
                    window.location.href='/';
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
        if(new Date(deadline.val()) < new Date()) {
            deadline.focus();
            alert("任务截止时间输入错误！");
            return false;
        }

        return true;
    }
});

function getUrlParam(name) {
    let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    let r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]);
    return null; //返回参数值
}