// 调试工具 - 检查功能是否正常
console.log('=== 保定旅游网 - 功能调试工具 ===');

// 检查CSRF Token
function checkCSRFToken() {
    var token = getCSRFToken();
    if (token) {
        console.log('✅ CSRF Token获取成功:', token.substring(0, 10) + '...');
        return true;
    } else {
        console.error('❌ CSRF Token获取失败！');
        return false;
    }
}

// 检查jQuery
function checkjQuery() {
    if (typeof jQuery !== 'undefined') {
        console.log('✅ jQuery已加载，版本:', jQuery.fn.jquery);
        return true;
    } else {
        console.error('❌ jQuery未加载！');
        return false;
    }
}

// 检查Bootstrap
function checkBootstrap() {
    if (typeof bootstrap !== 'undefined') {
        console.log('✅ Bootstrap已加载');
        return true;
    } else {
        console.error('❌ Bootstrap未加载！');
        return false;
    }
}

// 检查按钮是否存在
function checkButtons() {
    var checks = {
        favorite: $('#favoriteButton').length > 0
    };
    
    console.log('按钮检查:');
    console.log('  收藏按钮:', checks.favorite ? '✅' : '❌');
    
    return checks;
}

// 测试API连接
function testAPI(apiUrl, method, data) {
    return fetch(apiUrl, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: data ? JSON.stringify(data) : undefined
    })
    .then(response => {
        console.log('API响应状态:', response.status, response.statusText);
        return response.json();
    })
    .then(data => {
        console.log('API响应数据:', data);
        return data;
    })
    .catch(error => {
        console.error('API请求失败:', error);
        throw error;
    });
}

// 页面加载完成后运行检查
$(document).ready(function() {
    console.log('\n=== 开始功能检查 ===\n');
    
    // 基础检查
    var csrfOk = checkCSRFToken();
    var jqOk = checkjQuery();
    var bsOk = checkBootstrap();
    var buttons = checkButtons();
    
    console.log('\n=== 检查结果 ===');
    if (csrfOk && jqOk && bsOk) {
        console.log('✅ 基础环境正常');
    } else {
        console.error('❌ 基础环境异常，请检查！');
    }
    
    // 如果按钮存在，说明页面加载正常
    if (buttons.favorite) {
        console.log('✅ 按钮已加载');
    }
    
    console.log('\n=== 检查完成 ===\n');
    console.log('提示：如果功能不工作，请查看上面的错误信息');
    console.log('可以在浏览器控制台输入以下命令测试：');
    console.log('  testAPI("/api/v1/users/favorites/", "GET") - 测试收藏API');
    console.log('  checkCSRFToken() - 检查CSRF Token');
});

