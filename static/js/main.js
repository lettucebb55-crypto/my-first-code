// 全站通用的JavaScript文件

$(document).ready(function() {
    console.log("保定旅游网 - 页面加载完毕。");

    // 示例：表单验证 (例如登录/注册/预订表单)
    // 使用 Bootstrap 5 的验证样式
    (function () {
        'use strict'
        // 获取所有需要验证的表单
        var forms = document.querySelectorAll('.needs-validation')

        // 循环并阻止默认提交
        Array.prototype.slice.call(forms)
            .forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                    form.classList.add('was-validated')
                }, false)
            })
    })();


    // 示例：收藏按钮的 AJAX 切换 (在详情页)
    $("#favoriteButton").on("click", function() {
        // 假设需要登录
        // if (!is_authenticated) {
        //     // 弹出登录模态框
        //     $('#loginModal').modal('show');
        //     return;
        // }

        var $this = $(this);
        // 假设用 'active' class 标记是否已收藏
        var isFavorited = $this.hasClass('active');

        // 伪代码：发起AJAX请求
        // var api_url = isFavorited ? "URL_TO_UNFAVORITE" : "URL_TO_FAVORITE";
        // var method = isFavorited ? "DELETE" : "POST";

        console.log("模拟AJAX:", isFavorited ? "取消收藏" : "添加收藏");

        // $.ajax({
        //     url: api_url,
        //     method: method,
        //     data: { "target_id": 1, "target_type": "scenic" }, // 示例数据
        //     success: function(response) {
        //         if (response.status === 'success') {
                     if (isFavorited) {
                        $this.removeClass('active btn-danger').addClass('btn-outline-danger');
                        $this.html('<i class="far fa-heart"></i> 收藏');
                    } else {
                        $this.addClass('active btn-danger').removeClass('btn-outline-danger');
                        $this.html('<i class="fas fa-heart"></i> 已收藏');
                    }
        //         }
        //     }
        // });

        // --- 模拟切换 (无AJAX) ---
         if (isFavorited) {
            $this.removeClass('active btn-danger').addClass('btn-outline-danger');
            $this.html('<i class="far fa-heart"></i> 收藏');
        } else {
            $this.addClass('active btn-danger').removeClass('btn-outline-danger');
            $this.html('<i class="fas fa-heart"></i> 已收藏');
        }
        // --- 模拟结束 ---
    });

});