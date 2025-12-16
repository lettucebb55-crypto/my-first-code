// 一个帮助函数，用于获取 Django 的 CSRF token（多种方式尝试）
// 暴露到全局作用域，方便调试
window.getCSRFToken = function() {
    // 方法1: 从meta标签获取
    var token = document.querySelector('meta[name=csrf-token]');
    if (token) {
        return token.getAttribute('content');
    }
    
    // 方法2: 从cookie获取
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    var token = getCookie('csrftoken');
    if (token) {
        return token;
    }
    
    // 方法3: 从隐藏的input获取
    var tokenInput = document.querySelector('input[name=csrfmiddlewaretoken]');
    if (tokenInput) {
        return tokenInput.value;
    }
    
    console.error('无法获取CSRF token！');
    return null;
};
const csrftoken = window.getCSRFToken();


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


    // 收藏按钮的 AJAX 切换 (在详情页)
    $(document).on("click", "#favoriteButton", function() {
        var $this = $(this);
        // 支持多种属性名：spot-id/route-id/hotel-id 等
        var spotId = $this.data('spot-id') || $this.data('route-id') || $this.data('hotel-id') || $this.data('food-id');
        var spotType = $this.data('spot-type') || $this.data('route-type') || $this.data('hotel-type') || $this.data('food-type') || 'scenic';
        var isFavorited = $this.hasClass('active');
        
        // 检查是否已登录
        if (!csrftoken) {
            alert('请先登录！');
            window.location.href = '/users/login/';
            return;
        }

        // 确定API URL和方法
        var apiUrl = '/api/v1/users/favorites/';
        var method = isFavorited ? 'DELETE' : 'POST';
        
        console.log('收藏操作:', {spotId: spotId, spotType: spotType, isFavorited: isFavorited, method: method});

        // 构建请求配置
        var requestConfig = {
            method: method,
            headers: {
                'X-CSRFToken': csrftoken
            }
        };

        // DELETE请求通过URL参数传递，POST请求通过body传递
        if (method === 'DELETE') {
            apiUrl += '?target_id=' + spotId + '&target_type=' + spotType;
        } else {
            requestConfig.headers['Content-Type'] = 'application/json';
            requestConfig.body = JSON.stringify({
                target_id: spotId,
                target_type: spotType
            });
        }

        // 发送AJAX请求
        fetch(apiUrl, requestConfig)
        .then(response => {
            console.log('收藏响应状态:', response.status);
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || '请求失败');
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('收藏响应数据:', data);
            if (data.status === 'success') {
                // 更新按钮状态
                if (data.is_favorited) {
                    $this.addClass('active btn-danger').removeClass('btn-outline-danger');
                    $this.html('<i class="fas fa-heart"></i> 已收藏');
                } else {
                    $this.removeClass('active btn-danger').addClass('btn-outline-danger');
                    $this.html('<i class="far fa-heart"></i> 收藏');
                }
            } else {
                alert('操作失败：' + (data.message || '未知错误'));
            }
        })
        .catch(error => {
            console.error('收藏错误:', error);
            alert('操作失败：' + error.message);
        });
    });

    // 页面加载时检查收藏状态
    function checkFavoriteStatus() {
        var $favoriteBtn = $("#favoriteButton");
        if ($favoriteBtn.length > 0) {
            // 支持多种属性名
            var spotId = $favoriteBtn.data('spot-id') || $favoriteBtn.data('route-id') || $favoriteBtn.data('hotel-id') || $favoriteBtn.data('food-id');
            var spotType = $favoriteBtn.data('spot-type') || $favoriteBtn.data('route-type') || $favoriteBtn.data('hotel-type') || $favoriteBtn.data('food-type') || 'scenic';
            
            // 检查是否已收藏
            fetch(`/api/v1/users/favorites/?target_type=${spotType}`, {
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    var isFavorited = data.data.some(function(fav) {
                        return fav.target_id == spotId && fav.target_type === spotType;
                    });
                    
                    if (isFavorited) {
                        $favoriteBtn.addClass('active btn-danger').removeClass('btn-outline-danger');
                        $favoriteBtn.html('<i class="fas fa-heart"></i> 已收藏');
                    }
                }
            })
            .catch(error => {
                console.error('检查收藏状态失败:', error);
            });
        }
    }
    
    // 页面加载完成后检查收藏状态
    checkFavoriteStatus();
    

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