/**
 * Vue.js API 封装
 * 统一处理所有 API 请求，包括 CSRF token、错误处理等
 */

// 创建 Axios 实例
const apiClient = axios.create({
    baseURL: '/api/v1/',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// 请求拦截器：自动添加 CSRF token
apiClient.interceptors.request.use(
    function(config) {
        const csrfToken = window.getCSRFToken();
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
        return config;
    },
    function(error) {
        return Promise.reject(error);
    }
);

// 响应拦截器：统一处理错误
apiClient.interceptors.response.use(
    function(response) {
        return response;
    },
    function(error) {
        if (error.response) {
            // 服务器返回了错误状态码
            const status = error.response.status;
            const message = error.response.data?.message || error.response.data?.detail || '请求失败';
            
            if (status === 401) {
                // 未授权，可能需要登录
                window.showError('请先登录');
                // 可以重定向到登录页
                // window.location.href = '/users/login/';
            } else if (status === 403) {
                window.showError('没有权限执行此操作');
            } else if (status === 404) {
                window.showError('资源不存在');
            } else if (status === 500) {
                window.showError('服务器错误，请稍后重试');
            } else {
                window.showError(message);
            }
        } else if (error.request) {
            // 请求已发出但没有收到响应
            window.showError('网络错误，请检查网络连接');
        } else {
            // 其他错误
            window.showError('请求失败：' + error.message);
        }
        return Promise.reject(error);
    }
);

// API 方法封装
window.VueAPI = {
    // 景点相关 API
    scenic: {
        // 获取景点列表
        getList: (params = {}) => apiClient.get('/scenic/list/', { params }),
        // 获取景点详情
        getDetail: (id) => apiClient.get(`/scenic/${id}/`),
        // 搜索景点
        search: (keyword) => apiClient.get('/scenic/search/', { params: { q: keyword } }),
    },
    
    // 路线相关 API
    routes: {
        // 获取路线列表
        getList: (params = {}) => apiClient.get('/routes/list/', { params }),
        // 获取路线详情
        getDetail: (id) => apiClient.get(`/routes/${id}/`),
    },
    
    // 酒店相关 API
    hotels: {
        // 获取酒店列表
        getList: (params = {}) => apiClient.get('/hotels/list/', { params }),
        // 获取酒店详情
        getDetail: (id) => apiClient.get(`/hotels/${id}/`),
    },
    
    // 用户相关 API
    users: {
        // 获取用户信息
        getProfile: () => apiClient.get('/users/profile/'),
        // 更新用户信息
        updateProfile: (data) => apiClient.put('/users/profile/', data),
        // 获取收藏列表
        getFavorites: () => apiClient.get('/users/favorites/'),
        // 添加收藏
        addFavorite: (targetId, targetType) => apiClient.post('/users/favorites/', {
            target_id: targetId,
            target_type: targetType
        }),
        // 取消收藏
        removeFavorite: (targetId, targetType) => apiClient.delete('/users/favorites/', {
            params: { target_id: targetId, target_type: targetType }
        }),
        // 获取订单列表
        getOrders: (params = {}) => apiClient.get('/users/orders/', { params }),
        // 获取评价列表
        getReviews: () => apiClient.get('/users/reviews/'),
    },
    
    // 订单相关 API
    orders: {
        // 创建订单
        create: (data) => apiClient.post('/orders/create/', data),
        // 获取订单详情
        getDetail: (id) => apiClient.get(`/orders/${id}/`),
        // 取消订单
        cancel: (id) => apiClient.post(`/orders/${id}/cancel/`),
    },
    
    // 评论相关 API
    comments: {
        // 获取评论列表
        getList: (targetId, targetType) => apiClient.get('/comments/', {
            params: { target_id: targetId, target_type: targetType }
        }),
        // 创建评论
        create: (data) => apiClient.post('/comments/', data),
        // 删除评论
        delete: (commentId) => apiClient.delete(`/comments/${commentId}/`),
    },
    
    // 新闻相关 API
    news: {
        // 获取新闻列表
        getList: (params = {}) => apiClient.get('/news/list/', { params }),
        // 获取新闻详情
        getDetail: (id) => apiClient.get(`/news/${id}/`),
    },
    
    // 美食相关 API
    foods: {
        // 获取美食列表
        getList: (params = {}) => apiClient.get('/foods/list/', { params }),
        // 获取美食详情
        getDetail: (id) => apiClient.get(`/foods/${id}/`),
    },
};

