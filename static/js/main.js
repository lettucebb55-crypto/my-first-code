// 一个帮助函数，用于获取 Django 的 CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


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


    // 【新增】取消订单的 AJAX 逻辑
    // 我们使用事件委托，因为订单列表是动态加载的
    $('body').on('click', '.btn-cancel-order', function(event) {
        event.preventDefault(); // 阻止 href="#" 默认行为

        var $this = $(this);
        var orderSn = $this.data('order-sn');

        if (!orderSn) {
            alert('无法获取订单号');
            return;
        }

        if (!confirm("您确定要取消这个订单吗？")) {
            return;
        }

        fetch(`/api/v1/orders/cancel/${orderSn}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // 必须包含 CSRF token
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('订单已成功取消！');

                // 更新页面上的UI
                var $card = $this.closest('.card');
                // 找到状态文本并更新
                $card.find('.card-header span:last-child')
                     .text('已取消')
                     .removeClass('text-warning text-success')
                     .addClass('text-muted');

                // 替换整个按钮区域
                $this.closest('.card-footer').html('<a href="#" class="btn btn-sm btn-outline-secondary">查看详情</a>');
            } else {
                alert('操作失败: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('请求失败，请检查网络或联系管理员。');
        });
    });

});