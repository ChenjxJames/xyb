$(document).ready(function () {
    let sex = '0';      //发布任务性别限定（0:all, 1:man, 2:woman）
    $("#visible_list").hide();

    $("body").click(function () {
        $("#visible_list").hide();
    });

    $("#set_visible").click(function (event) {
       $("#visible_list").show();
        event.stopPropagation();
    });

    //设置为全部人可见
    $("#visible_all").click(function () {
        $("#set_visible>span").text("公开")
        sex = 0;
    });

    //设置为仅男生可见
    $("#visible_male").click(function () {
        $("#set_visible>span").text("仅男生可见");
        sex = 1;
    });

    //设置为仅女生可见
    $("#visible_female").click(function () {
        $("#set_visible>span").text("仅女生可见");
        sex = 2;
    });

    //发布任务按钮单击
    $("#btn_add_task_submit").click(function () {
        if (createTaskIsValid()) {
            createTaskAjax();
        }
    });

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