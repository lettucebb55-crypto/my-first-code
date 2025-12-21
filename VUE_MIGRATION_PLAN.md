# Vue.js 前端迁移计划

## 迁移策略

采用**渐进式迁移**策略，逐步将页面从 Django 模板 + jQuery 迁移到 Vue.js，保持现有功能可用。

## 技术栈

- **Vue.js 3** (CDN 方式，与 AI 助手保持一致)
- **Axios** (HTTP 客户端)
- **Vue Router** (可选，用于单页应用路由)
- **Bootstrap 5** (保持现有 UI 框架)
- **Django REST API** (后端提供数据接口)

## 迁移步骤

### 第一阶段：基础架构搭建 ✅
1. 在 `base.html` 中统一引入 Vue.js 和相关依赖
2. 创建 Vue 工具函数（API 调用、CSRF 处理等）
3. 创建 Vue 组件目录结构

### 第二阶段：核心页面迁移
1. 首页 (`index/index.html`)
2. 景点列表和详情页 (`scenic/list.html`, `scenic/detail.html`)
3. 路线列表和详情页 (`routes/list.html`, `routes/detail.html`)
4. 酒店列表和详情页 (`hotels/list.html`, `hotels/detail.html`)

### 第三阶段：用户中心迁移
1. 用户首页 (`user/home.html`)
2. 我的订单 (`user/orders.html`)
3. 我的收藏 (`user/favorites.html`)
4. 我的评价 (`user/reviews.html`)
5. 个人资料 (`user/profile.html`)

### 第四阶段：其他页面迁移
1. 订单相关页面 (`orders/confirm.html`, `orders/detail.html`)
2. 新闻列表和详情页 (`news/list.html`, `news/detail.html`)
3. 美食列表和详情页 (`foods/list.html`, `foods/detail.html`)

### 第五阶段：优化和清理
1. 移除 jQuery 依赖（如果不再需要）
2. 优化 Vue 组件性能
3. 统一代码风格和规范

## 文件结构

```
static/
├── js/
│   ├── main.js              # 通用工具函数（保留）
│   ├── vue/
│   │   ├── app.js           # Vue 应用入口
│   │   ├── api.js           # API 调用封装
│   │   ├── utils.js         # 工具函数
│   │   └── components/      # Vue 组件
│   │       ├── ScenicList.vue
│   │       ├── ScenicDetail.vue
│   │       ├── RouteList.vue
│   │       └── ...
```

## 注意事项

1. **保持向后兼容**：迁移过程中，旧页面和新页面可以并存
2. **API 优先**：确保所有数据通过 API 获取，不依赖 Django 模板变量
3. **渐进增强**：先迁移简单页面，再迁移复杂页面
4. **测试充分**：每个页面迁移后都要充分测试

## 当前状态

- ✅ AI 助手已使用 Vue.js
- 🔄 开始基础架构搭建
- ⏳ 等待迁移其他页面

