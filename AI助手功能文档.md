# AI助手功能完整文档

## 📋 目录

1. [功能概述](#功能概述)
2. [技术架构](#技术架构)
3. [数据模型](#数据模型)
4. [API接口文档](#api接口文档)
5. [前端使用说明](#前端使用说明)
6. [后端实现说明](#后端实现说明)
7. [AI服务集成指南](#ai服务集成指南)
8. [使用示例](#使用示例)
9. [常见问题](#常见问题)
10. [开发指南](#开发指南)

---

## 功能概述

AI助手是保定旅游网的核心智能功能模块，旨在为用户提供个性化的旅游规划服务。用户只需输入想要游览的景点名称，AI助手即可智能生成：

- **路线规划**：合理安排景点的游览顺序、时间分配和行程安排
- **交通规划**：提供自驾、公共交通、包车等交通方式建议
- **旅游策略**：提供时间安排、门票预订、最佳游览时间、必备物品、注意事项等建议

### 核心特性

✅ **智能景点匹配**：支持多种景点名称匹配方式（精确匹配、模糊匹配、智能去后缀匹配）  
✅ **多种规划类型**：支持综合规划、路线规划、交通规划、旅游策略四种类型  
✅ **查询历史保存**：登录用户可查看历史查询记录  
✅ **规划结果收藏**：支持收藏喜欢的规划结果  
✅ **规划结果导出**：支持导出为文本文件  
✅ **实时响应**：基于规则引擎，响应速度快，无需等待  
✅ **免费使用**：当前版本使用规则引擎，完全免费，无需API密钥  

---

## 技术架构

### 整体架构

```
┌─────────────────┐
│   前端 (Vue.js) │
│  - 用户交互界面  │
│  - 数据展示     │
└────────┬────────┘
         │ HTTP/JSON
         ▼
┌─────────────────┐
│  Django后端API  │
│  - 请求处理     │
│  - 景点查询     │
│  - 规划生成     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   规划引擎      │
│  - 规则引擎     │
│  - (可选)AI API │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   数据库        │
│  - 景点数据     │
│  - 查询历史     │
└─────────────────┘
```

### 技术栈

**前端技术：**
- Vue.js 3（通过CDN引入）
- Axios（HTTP请求）
- Marked（Markdown解析）
- Bootstrap 5（UI框架）

**后端技术：**
- Django 4.2+
- Django REST API
- SQLite/PostgreSQL（数据库）

**规划引擎：**
- 当前：基于规则的规划引擎
- 可选：OpenAI、百度文心一言、阿里通义千问等

---

## 数据模型

### AIQuery 模型

位于 `apps/ai_assistant/models.py`，用于保存用户的AI查询记录。

#### 字段说明

| 字段名 | 类型 | 说明 | 是否必填 |
|--------|------|------|----------|
| `user` | ForeignKey | 用户（可为空，支持未登录用户） | 否 |
| `query_type` | CharField | 查询类型 | 是 |
| `scenic_spots` | TextField | 景点列表（JSON格式） | 是 |
| `user_input` | TextField | 用户输入内容 | 是 |
| `route_plan` | TextField | 路线规划结果 | 否 |
| `transport_plan` | TextField | 交通规划结果 | 否 |
| `strategy_plan` | TextField | 旅游策略结果 | 否 |
| `full_response` | TextField | 完整AI响应（JSON格式） | 否 |
| `created_at` | DateTimeField | 创建时间 | 是（自动） |
| `is_favorite` | BooleanField | 是否收藏 | 是（默认False） |

#### 查询类型（query_type）

- `route`：路线规划
- `transport`：交通规划
- `strategy`：旅游策略
- `general`：综合规划（包含以上所有）

#### 示例数据

```json
{
  "user": 1,
  "query_type": "general",
  "scenic_spots": "[{\"id\": 1, \"name\": \"白洋淀\", \"address\": \"保定市安新县\", ...}]",
  "user_input": "希望行程不要太紧张",
  "route_plan": "## 一日游路线规划\n\n...",
  "transport_plan": "## 交通规划\n\n...",
  "strategy_plan": "## 旅游策略建议\n\n...",
  "created_at": "2025-01-15 10:30:00",
  "is_favorite": false
}
```

---

## API接口文档

### 基础URL

所有API接口的基础路径：`/api/v1/ai-assistant/`

### 1. 生成AI规划

**接口：****`POST /api/v1/ai-assistant/plan/`**

**功能：**根据用户输入的景点，生成AI规划

**请求头：**
```
Content-Type: application/json
X-CSRFToken: <csrf_token>
```

**请求体：**
```json
{
  "scenic_spots": ["白洋淀", "直隶总督署", "古莲花池"],
  "query_type": "general",
  "user_input": "希望行程不要太紧张，适合老人和小孩"
}
```

**参数说明：**

| 参数 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `scenic_spots` | Array | 景点名称列表 | 是 |
| `query_type` | String | 规划类型：`general`/`route`/`transport`/`strategy` | 否（默认`general`） |
| `user_input` | String | 用户额外需求 | 否 |

**响应示例（成功）：**
```json
{
  "status": "success",
  "data": {
    "scenic_spots": [
      {
        "id": 1,
        "name": "白洋淀",
        "address": "保定市安新县",
        "ticket_price": "50.00",
        "open_time": "08:00-18:00",
        "description": "白洋淀是华北地区最大的淡水湖...",
        "latitude": 38.9,
        "longitude": 115.9
      }
    ],
    "plan": {
      "route_plan": "## 一日游路线规划\n\n...",
      "transport_plan": "## 交通规划\n\n...",
      "strategy_plan": "## 旅游策略建议\n\n..."
    },
    "query_id": 123,
    "is_favorite": false
  }
}
```

**响应示例（错误）：**
```json
{
  "status": "error",
  "message": "请至少输入一个景点"
}
```

**状态码：**
- `200`：成功
- `400`：请求参数错误
- `404`：未找到匹配的景点
- `500`：服务器错误

---

### 2. 获取查询历史

**接口：****`GET /api/v1/ai-assistant/history/`**

**功能：**获取当前登录用户的查询历史（最近20条）

**权限：**需要登录

**请求头：**
```
X-CSRFToken: <csrf_token>
```

**响应示例：**
```json
{
  "status": "success",
  "data": [
    {
      "id": 123,
      "query_type": "general",
      "query_type_display": "综合规划",
      "user_input": "规划白洋淀、直隶总督署的旅游",
      "created_at": "2025-01-15 10:30:00",
      "is_favorite": false
    }
  ]
}
```

---

### 3. 获取查询详情

**接口：****`GET /api/v1/ai-assistant/query/<query_id>/`**

**功能：**获取指定查询的详细信息

**权限：**需要登录，且只能查看自己的查询记录

**响应示例：**
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "query_type": "general",
    "query_type_display": "综合规划",
    "user_input": "规划白洋淀、直隶总督署的旅游",
    "scenic_spots": [...],
    "route_plan": "## 一日游路线规划\n\n...",
    "transport_plan": "## 交通规划\n\n...",
    "strategy_plan": "## 旅游策略建议\n\n...",
    "created_at": "2025-01-15 10:30:00",
    "is_favorite": false
  }
}
```

---

### 4. 收藏/取消收藏

**接口：****`POST /api/v1/ai-assistant/query/<query_id>/favorite/`**（收藏）  
**接口：****`DELETE /api/v1/ai-assistant/query/<query_id>/favorite/`**（取消收藏）

**功能：**收藏或取消收藏规划结果

**权限：**需要登录

**响应示例：**
```json
{
  "status": "success",
  "message": "收藏成功",
  "is_favorite": true
}
```

---

### 5. 导出规划结果

**接口：****`GET /api/v1/ai-assistant/query/<query_id>/export/`**

**功能：**导出规划结果为文本文件

**权限：**需要登录

**响应：**返回文本文件（`.txt`格式），文件名格式：`ai_plan_<query_id>.txt`

---

## 前端使用说明

### 页面访问

访问路径：`/ai-assistant/`

### 功能操作

#### 1. 输入景点信息

- 在"景点名称"输入框中输入景点名称
- 支持多个景点，用逗号（`,`）、中文逗号（`，`）或换行分隔
- 系统会自动解析并显示已输入的景点数量

#### 2. 选择规划类型

- **综合规划**：包含路线、交通、策略的完整规划
- **路线规划**：仅生成路线安排
- **交通规划**：仅生成交通建议
- **旅游策略**：仅生成策略建议

#### 3. 输入额外需求（可选）

- 在"额外需求"输入框中输入特殊要求
- 例如："希望行程不要太紧张"、"适合老人和小孩"等

#### 4. 生成规划

- 点击"生成AI规划"按钮
- 系统会显示加载状态
- 规划结果会在右侧显示

#### 5. 查看历史记录（需登录）

- 登录用户可以在左侧看到最近5条查询历史
- 点击历史记录可以重新加载该规划
- 点击"查看全部历史"可查看完整历史记录

#### 6. 收藏规划（需登录）

- 在规划结果上方点击"收藏"按钮
- 收藏的规划可以在历史记录中查看

#### 7. 导出规划（需登录）

- 点击"导出规划"按钮
- 系统会下载一个文本文件，包含完整的规划内容

### Vue组件说明

主要Vue组件位于 `templates/ai_assistant/index.html`，使用Vue 3 Composition API风格。

#### 主要数据属性

```javascript
{
  scenicInput: '',        // 用户输入的景点文本
  scenicSpots: [],        // 解析后的景点列表
  queryType: 'general',   // 规划类型
  userInput: '',          // 用户额外需求
  loading: false,         // 加载状态
  error: null,            // 错误信息
  planResult: null,       // 规划结果
  warning: null,          // 警告信息
  history: [],            // 查询历史
  isAuthenticated: false  // 是否已登录
}
```

#### 主要方法

- `parseScenicSpots()`：解析输入的景点名称
- `generatePlan()`：生成AI规划
- `loadHistory()`：加载查询历史
- `loadHistoryItem(queryId)`：加载指定历史记录
- `toggleFavorite(queryId)`：切换收藏状态
- `exportPlan(queryId)`：导出规划结果
- `formatMarkdown(text)`：格式化Markdown文本为HTML

---

## 后端实现说明

### 核心文件

- **`apps/ai_assistant/models.py`**：数据模型定义
- **`apps/ai_assistant/api.py`**：API视图实现
- **`apps/ai_assistant/views.py`**：页面视图
- **`apps/ai_assistant/urls.py`**：URL路由配置
- **`apps/ai_assistant/api_urls.py`**：API路由配置

### 景点匹配逻辑

位于 `apps/ai_assistant/api.py` 的 `AIPlanAPIView.post()` 方法中，采用三级匹配策略：

1. **精确匹配**：直接匹配景点名称
2. **包含匹配**：使用 `name__icontains` 进行模糊匹配
3. **智能去后缀匹配**：去掉"景区"、"公园"、"景点"等常见后缀后匹配

```python
# 示例代码
spot = ScenicSpot.objects.filter(name=name).first()  # 精确匹配
if not spot:
    spot = ScenicSpot.objects.filter(name__icontains=name).first()  # 模糊匹配
if not spot:
    # 去掉后缀后匹配
    name_variants = [
        name.replace('景区', '').replace('公园', '').replace('景点', '').strip(),
        name.replace('旅游区', '').replace('风景区', '').strip(),
    ]
    for variant in name_variants:
        spot = ScenicSpot.objects.filter(name__icontains=variant).first()
        if spot:
            break
```

### 规划生成逻辑

位于 `apps/ai_assistant/api.py` 的 `_generate_plan()` 方法中，当前使用规则引擎生成规划。

#### 路线规划生成（`_generate_route_plan()`）

- **单景点**：生成一日游规划，包含上午、中午、下午、傍晚的时间安排
- **多景点（一天）**：如果用户要求一天完成，将所有景点紧凑安排在同一天
- **多景点（多天）**：默认每个景点安排一天，生成多日游规划

#### 交通规划生成（`_generate_transport_plan()`）

- 提供自驾、公共交通、包车/租车三种交通方式建议
- 根据景点数量提供不同的交通规划

#### 旅游策略生成（`_generate_strategy_plan()`）

- 时间安排建议
- 门票预订建议（包含总费用计算）
- 最佳游览时间建议
- 必备物品清单
- 注意事项提醒
- 用户特殊需求处理

---

## AI服务集成指南

当前版本使用规则引擎生成规划，功能完整且免费。如需更智能的规划，可以集成真实的AI服务。

### 集成步骤

详细集成指南请参考：`apps/ai_assistant/AI_API_INTEGRATION.md`

#### 支持的AI服务

1. **OpenAI API**（GPT-3.5/GPT-4）
2. **百度文心一言**
3. **阿里通义千问**
4. **其他兼容OpenAI API格式的服务**

#### 集成要点

1. **安装依赖**：根据选择的AI服务安装相应的Python库
2. **配置API密钥**：在 `settings.py` 中配置（建议使用环境变量）
3. **修改代码**：在 `apps/ai_assistant/api.py` 的 `_generate_plan()` 方法中调用AI API
4. **错误处理**：实现回退机制，AI API失败时使用规则引擎
5. **成本控制**：添加缓存或限制调用频率

### 配置开关

可以在 `settings.py` 中添加配置开关：

```python
# AI配置
USE_AI_API = False  # True时使用AI API，False时使用规则引擎
AI_PROVIDER = 'openai'  # 'openai', 'qianfan', 'dashscope'
```

---

## 使用示例

### 示例1：单景点一日游

**输入：**
- 景点：白洋淀
- 规划类型：综合规划

**输出：**
- 路线规划：包含上午、中午、下午、傍晚的详细时间安排
- 交通规划：提供自驾、公共交通、包车建议
- 旅游策略：时间安排、门票预订、必备物品等建议

### 示例2：多景点多日游

**输入：**
- 景点：白洋淀, 直隶总督署, 古莲花池
- 规划类型：综合规划
- 额外需求：希望行程不要太紧张

**输出：**
- 路线规划：3天行程，每天游览1个景点
- 交通规划：各景点之间的交通方式建议
- 旅游策略：包含总门票费用、最佳游览时间等

### 示例3：多景点一日游

**输入：**
- 景点：直隶总督署, 古莲花池
- 规划类型：路线规划
- 额外需求：一天完成

**输出：**
- 路线规划：紧凑的一日游安排，上午游览一个景点，下午游览另一个景点

---

## 常见问题

### Q1: 输入的景点找不到怎么办？

**A:** 系统会尝试多种匹配方式：
1. 精确匹配景点名称
2. 模糊匹配（包含关键词）
3. 智能去后缀匹配（去掉"景区"、"公园"等后缀）

如果仍然找不到，请检查：
- 景点名称是否正确
- 景点是否已录入系统
- 可以尝试输入景点的简称或别名

### Q2: 为什么规划结果不够智能？

**A:** 当前版本使用规则引擎生成规划，虽然功能完整，但智能化程度有限。如需更智能的规划，可以：
1. 集成真实的AI服务（OpenAI、百度文心一言等）
2. 参考 `apps/ai_assistant/AI_API_INTEGRATION.md` 进行集成

### Q3: 未登录用户可以使用吗？

**A:** 可以。未登录用户可以使用所有规划功能，但无法：
- 保存查询历史
- 收藏规划结果
- 导出规划结果

建议注册登录以获得完整功能体验。

### Q4: 如何集成OpenAI API？

**A:** 详细步骤请参考 `apps/ai_assistant/AI_API_INTEGRATION.md`，主要步骤：
1. 安装 `openai` 库
2. 在 `settings.py` 中配置API密钥
3. 修改 `apps/ai_assistant/api.py` 的 `_generate_plan()` 方法

### Q5: 规划结果可以导出为PDF吗？

**A:** 当前版本仅支持导出为文本文件（`.txt`）。如需PDF导出，可以：
1. 安装 `reportlab` 或 `weasyprint` 库
2. 在 `AIQueryExportAPIView` 中添加PDF生成逻辑

### Q6: 如何提高规划质量？

**A:** 可以：
1. 在"额外需求"中详细描述您的需求
2. 输入准确的景点名称
3. 集成真实的AI服务
4. 在数据库中补充更详细的景点信息（距离、交通路线等）

---

## 开发指南

### 添加新功能

#### 1. 添加新的规划类型

在 `apps/ai_assistant/models.py` 中修改 `query_type` 的 choices：

```python
query_type = models.CharField(max_length=20, choices=[
    ('route', '路线规划'),
    ('transport', '交通规划'),
    ('strategy', '旅游策略'),
    ('general', '综合规划'),
    ('new_type', '新规划类型'),  # 添加新类型
], default='general')
```

在 `apps/ai_assistant/api.py` 中添加对应的生成方法。

#### 2. 优化景点匹配

可以在 `AIPlanAPIView.post()` 方法中：
- 添加同义词匹配
- 添加拼音匹配
- 添加模糊搜索算法（如Levenshtein距离）

#### 3. 添加缓存机制

对于相同的查询，可以添加缓存以避免重复计算：

```python
from django.core.cache import cache

cache_key = f"ai_plan_{hash(str(scenic_spots) + query_type + user_input)}"
cached_result = cache.get(cache_key)
if cached_result:
    return cached_result
```

#### 4. 添加统计功能

可以添加统计功能，记录：
- 最受欢迎的景点
- 最常用的规划类型
- 用户查询频率

### 代码规范

- 遵循PEP 8 Python代码规范
- 使用有意义的变量和函数名
- 添加必要的注释和文档字符串
- 处理异常情况，提供友好的错误提示

### 测试建议

1. **单元测试**：测试各个规划生成方法
2. **集成测试**：测试完整的API流程
3. **前端测试**：测试Vue组件的交互
4. **性能测试**：测试大量并发请求的处理能力

---

## 总结

AI助手模块是保定旅游网的核心智能功能，通过规则引擎或真实AI服务，为用户提供个性化的旅游规划服务。当前版本功能完整，支持多种规划类型、查询历史、收藏导出等功能。如需更智能的规划，可以按照集成指南接入真实的AI服务。

---

**文档版本：** v1.0  
**最后更新：** 2025年1月  
**维护者：** 保定旅游网开发团队

