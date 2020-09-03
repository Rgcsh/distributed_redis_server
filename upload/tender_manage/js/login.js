$(function () {
    $('[data-toggle="popover"]').popover()
    $("#form_login").validate({
        rules: {
            email: {
                required: true
            },
            regPass: {
                required: true
            }
        },
        messages: {
            email: {
                required: "请输入邮箱"
            },
            regPass: {
                required: "请输入密码"
            }
        },
        submitHandler: function () {
            disabled_click(this);
            var email = $("#login_email").val().toLowerCase(); //邮箱
            var password = $("#login_password").val(); //密码
            //登录接口
            $.ajax({
                url: serverUrl_user + "login",
                type: 'post',
                dataType: "json",
                data: {
                    email: email,
                    password: password
                },
                success: function (data) {
                    if (data.respCode == 200) {
						login_cookies_set(data)
                        window.location.href = serverUrl_weburl + "main.html";
                    } else {
                        hide_popover('#login_button', data.respMsg)
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus)
                    hide_popover('#login_button', '程序错误,请联系管理员')
                }
            });
        }
    });

    $(document).ready(function () {
        $("#form_login").validate({
            rules: {
                confirmPass: {
                    required: true,
                    minlength: 6,
                    equalTo: "#regPass"
                }
            },
            messages: {
                confirmPass: {
                    required: "请输入密码",
                    minlength: "密码长度不能小于 6 个字母",
                    equalTo: "两次密码输入不一致"
                }
            }
        });
        $("#login_button").click(function () {
            $("#login_button").submit();

        });
        $(document).keyup(function (e) {
            if (e.keyCode == 13) {
                $("#login_button").submit();
            }
        });
    });

});