/**
 * Vue.js 工具函数
 * 提供通用的工具方法，供所有 Vue 组件使用
 */

// 获取 CSRF Token
window.getCSRFToken = function() {
    // 方法1: 从meta标签获取
    const token = document.querySelector('meta[name=csrf-token]');
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
    
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
        return csrfToken;
    }
    
    // 方法3: 从隐藏的input获取
    const tokenInput = document.querySelector('input[name=csrfmiddlewaretoken]');
    if (tokenInput) {
        return tokenInput.value;
    }
    
    console.error('无法获取CSRF token！');
    return null;
};

// 格式化日期
window.formatDate = function(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};

// 格式化日期时间
window.formatDateTime = function(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}`;
};

// 格式化价格
window.formatPrice = function(price) {
    if (price === null || price === undefined) return '¥0.00';
    return `¥${parseFloat(price).toFixed(2)}`;
};

// 截断文本
window.truncateText = function(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
};

// 获取图片 URL（处理媒体文件）
window.getImageUrl = function(imagePath) {
    if (!imagePath) return '/static/images/placeholder.jpg';
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        return imagePath;
    }
    // 如果是相对路径，添加 MEDIA_URL
    if (imagePath.startsWith('/')) {
        return imagePath;
    }
    return '/media/' + imagePath;
};

// 显示成功消息
window.showSuccess = function(message) {
    // 可以使用 Bootstrap 的 Toast 或 Alert
    if (typeof bootstrap !== 'undefined') {
        // 创建 Toast 提示
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-success border-0';
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    } else {
        alert(message);
    }
};

// 显示错误消息
window.showError = function(message) {
    if (typeof bootstrap !== 'undefined') {
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-danger border-0';
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    } else {
        alert(message);
    }
};

// 确认对话框
window.confirmAction = function(message) {
    return confirm(message);
};

