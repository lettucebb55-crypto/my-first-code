# 保定旅游网

一个基于Django的旅游信息管理系统，提供景点浏览、路线规划、酒店预订、美食推荐、AI智能规划等功能。

## 项目概述

保定旅游网是一个综合性的旅游服务平台，旨在为游客提供全方位的旅游信息服务，包括：

- **景点信息**：浏览保定热门景点，查看详细信息、门票价格、开放时间等
- **路线规划**：查看精心设计的旅游路线，支持在线报名
- **酒店预订**：浏览推荐酒店，在线预订房间
- **美食文化**：了解保定特色美食和文化背景
- **旅游资讯**：获取最新的旅游新闻和资讯
- **AI智能助手**：根据用户输入的景点，智能规划路线、交通方式和旅游策略
- **个人中心**：管理订单、收藏、评价等个人信息

## 技术栈

### 后端
- **Django 4.2+**：Web框架
- **SQLite**：数据库（开发环境）
- **Django ORM**：数据库操作

### 前端
- **Bootstrap 5**：UI框架
- **Vue.js 3**：前端框架（AI助手模块）
- **jQuery**：DOM操作和AJAX请求
- **Font Awesome**：图标库
- **Axios**：HTTP客户端（Vue组件中使用）

## 项目结构

```
baoding_tourism/
├── apps/                    # Django应用目录
│   ├── users/              # 用户管理
│   ├── scenic/             # 景点管理
│   ├── routes/             # 路线管理
│   ├── hotels/              # 酒店管理
│   ├── foods/               # 美食管理
│   ├── news/                # 新闻资讯
│   ├── orders/              # 订单管理
│   ├── comments/            # 评论管理
│   ├── checkins/            # 打卡签到
│   ├── admin_panel/         # 后台管理
│   ├── index/               # 首页
│   └── ai_assistant/        # AI助手（新增）
├── templates/               # 模板文件
├── static/                  # 静态文件
├── media/                   # 媒体文件
├── baoding_tourism/         # 项目配置
└── manage.py               # Django管理脚本
```

## 功能模块

### 1. 用户模块（apps/users）
- 用户注册、登录、退出
- 个人中心
- 订单管理
- 收藏管理
- 评价管理

### 2. 景点模块（apps/scenic）
- 景点列表浏览
- 景点详情查看
- 景点分类筛选
- 景点搜索

### 3. 路线模块（apps/routes）
- 路线列表浏览
- 路线详情查看
- 路线报名
- 路线分类

### 4. 酒店模块（apps/hotels）
- 酒店列表浏览
- 酒店详情查看
- 房间类型选择
- 酒店预订（支持入住/退房日期选择）

### 5. 美食模块（apps/foods）
- 美食列表浏览
- 美食详情查看
- 美食分类
- 美食文化介绍

### 6. 订单模块（apps/orders）
- 订单创建
- 订单确认
- 订单支付
- 订单管理
- 订单状态跟踪

### 7. AI助手模块（apps/ai_assistant）✨ 新增功能

#### 功能说明
AI助手可以根据用户输入的景点名称，智能生成：
- **路线规划**：合理安排景点的游览顺序和时间
- **交通规划**：提供自驾、公共交通、包车等交通方式建议
- **旅游策略**：提供时间安排、门票预订、最佳游览时间、必备物品、注意事项等建议

#### 使用方法
1. 访问 `/ai-assistant/` 进入AI助手页面
2. 在左侧输入框输入景点名称（支持多个景点，用逗号分隔）
3. 选择规划类型：
   - **综合规划**：包含路线、交通、策略的完整规划
   - **路线规划**：仅生成路线安排
   - **交通规划**：仅生成交通建议
   - **旅游策略**：仅生成策略建议
4. 可选的额外需求输入框，输入特殊要求
5. 点击"生成AI规划"按钮
6. 在右侧查看生成的规划结果

#### 技术实现
- **前端**：使用Vue.js 3构建交互式界面
- **后端**：Django REST API提供数据接口
- **数据存储**：保存用户查询历史（需登录）
- **AI引擎**：
  - **当前版本**：使用规则引擎生成规划（免费，无需API密钥）
  - **可选升级**：可集成真实AI服务（OpenAI、百度文心一言、阿里通义千问等）
  - **集成说明**：详见 `apps/ai_assistant/AI_API_INTEGRATION.md`

#### API接口
- `POST /api/v1/ai-assistant/plan/`：生成AI规划
- `GET /api/v1/ai-assistant/history/`：获取查询历史（需登录）
- `GET /api/v1/ai-assistant/query/<id>/`：获取查询详情（需登录）
- `POST /api/v1/ai-assistant/query/<id>/favorite/`：收藏规划结果（需登录）
- `DELETE /api/v1/ai-assistant/query/<id>/favorite/`：取消收藏（需登录）
- `GET /api/v1/ai-assistant/query/<id>/export/`：导出规划结果为文本文件（需登录）

#### 功能特性
- ✅ 智能路线规划
- ✅ 交通方式建议
- ✅ 旅游策略推荐
- ✅ 查询历史保存（登录用户）
- ✅ 规划结果收藏
- ✅ 规划结果导出（文本格式）

### 8. 后台管理（apps/admin_panel）
- 用户管理
- 景点管理
- 路线管理
- 酒店管理
- 美食管理
- 订单管理
- 评论管理
- 新闻管理

## 安装和运行

### 环境要求
- Python 3.8+
- Django 4.2+

### 安装步骤

1. **克隆项目**
```bash
cd baoding_tourism
```

2. **安装依赖**
```bash
pip install django
```

3. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **创建超级用户**
```bash
python manage.py createsuperuser
```

5. **运行开发服务器**
```bash
python manage.py runserver
```

6. **访问系统**
- 前端：http://127.0.0.1:8000/
- 后台管理：http://127.0.0.1:8000/admin_panel/
- AI助手：http://127.0.0.1:8000/ai-assistant/

## 配置说明

### settings.py 主要配置
- `AUTH_USER_MODEL = 'users.CustomUser'`：使用自定义用户模型
- `LOGIN_URL = '/users/login/'`：登录页面URL
- `MEDIA_URL = '/media/'`：媒体文件URL
- `STATIC_URL = 'static/'`：静态文件URL

## 前端技术说明

### Vue.js集成
项目采用**渐进式集成**的方式引入Vue.js：
- 在AI助手模块中使用Vue.js 3（通过CDN）
- 其他页面继续使用jQuery和Bootstrap
- 这种方式的优点：
  - 不影响现有功能
  - 可以逐步迁移
  - 降低风险

### Vue组件位置
- `templates/ai_assistant/index.html`：AI助手主页面
- `templates/ai_assistant/history.html`：查询历史页面

### Vue相关库
- **Vue.js 3**：https://unpkg.com/vue@3/dist/vue.global.js
- **Axios**：https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js
- **Marked**：https://cdn.jsdelivr.net/npm/marked/marked.min.js（Markdown解析）

## 数据库模型

### AI助手相关模型
- **AIQuery**：保存用户的AI查询记录
  - `user`：用户（可为空，支持未登录用户）
  - `query_type`：查询类型（route/transport/strategy/general）
  - `scenic_spots`：景点列表（JSON格式）
  - `user_input`：用户输入内容
  - `route_plan`：路线规划结果
  - `transport_plan`：交通规划结果
  - `strategy_plan`：旅游策略结果
  - `created_at`：创建时间
  - `is_favorite`：是否收藏

## 开发指南

### 添加新功能
1. 在相应的app中创建models、views、urls
2. 创建对应的模板文件
3. 如需API，创建api.py和api_urls.py
4. 更新主urls.py

### 前端开发
- 使用Bootstrap 5进行样式设计
- 使用jQuery处理DOM操作和AJAX
- AI助手模块使用Vue.js 3
- 所有API请求需要包含CSRF token

### CSRF Token处理
- 在base.html中添加了`<meta name="csrf-token">`标签
- Vue组件通过`getCSRFToken()`方法获取token
- 所有POST请求需要在headers中包含`X-CSRFToken`

## 后续优化方向

### AI助手功能增强
1. **集成真实AI服务**：
   - 可以集成OpenAI API、百度文心一言、阿里通义千问等
   - 在`apps/ai_assistant/api.py`的`_generate_plan`方法中替换规则引擎

2. **功能扩展**：
   - 支持天气查询
   - 支持实时路况
   - 支持个性化推荐
   - 支持语音输入

3. **用户体验优化**：
   - 添加规划结果导出功能（PDF/图片）
   - 支持规划结果分享
   - 添加规划结果收藏功能

### 前端迁移
- 可以逐步将其他页面迁移到Vue.js
- 考虑使用Vue Router实现单页应用（SPA）
- 可以考虑使用Vue CLI或Vite构建工具

## 常见问题

### Q: AI助手生成的规划不够智能？
A: 当前版本使用规则引擎生成基础规划。如需更智能的规划，可以：
1. 集成真实的AI服务（如OpenAI API）
2. 在`apps/ai_assistant/api.py`中修改`_generate_plan`方法
3. 添加更多数据源（如景点距离、交通路线等）

### Q: 如何集成OpenAI API？
A: 在`apps/ai_assistant/api.py`中：
1. 安装openai库：`pip install openai`
2. 在settings.py中添加API密钥配置
3. 在`_generate_plan`方法中调用OpenAI API

### Q: Vue.js和jQuery可以共存吗？
A: 可以。项目采用渐进式集成，Vue.js只在AI助手模块使用，其他页面继续使用jQuery。

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请联系项目维护者。

---

**最后更新**：2025年12月

