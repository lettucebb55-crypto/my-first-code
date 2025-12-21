# AI API 集成指南

本文档说明如何将真实的AI服务（如OpenAI、百度文心一言等）集成到AI助手模块中。

## 当前实现

目前AI助手使用**规则引擎**生成规划，位于 `apps/ai_assistant/api.py` 的 `_generate_plan` 方法中。

## 集成真实AI API

### 方案1：集成OpenAI API

#### 1. 安装依赖

```bash
pip install openai
```

#### 2. 配置API密钥

在 `baoding_tourism/settings.py` 中添加：

```python
# AI配置
OPENAI_API_KEY = 'your-openai-api-key-here'  # 从环境变量读取更安全
OPENAI_MODEL = 'gpt-3.5-turbo'  # 或 'gpt-4'
```

**安全提示**：建议使用环境变量：

```python
import os
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
```

#### 3. 修改 `apps/ai_assistant/api.py`

在文件顶部添加：

```python
import openai
from django.conf import settings

# 初始化OpenAI客户端
if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
```

修改 `_generate_plan` 方法：

```python
def _generate_plan(self, scenic_spots, query_type, user_input):
    """
    生成旅游规划 - 使用OpenAI API
    """
    # 构建提示词
    scenic_names = [spot['name'] for spot in scenic_spots]
    prompt = f"""
你是一个专业的旅游规划助手。请根据以下信息为用户规划旅游：

景点列表：{', '.join(scenic_names)}
"""
    
    if query_type == 'route' or query_type == 'general':
        prompt += "\n请提供详细的路线规划，包括每天的行程安排、游览顺序、时间分配。"
    
    if query_type == 'transport' or query_type == 'general':
        prompt += "\n请提供交通规划，包括如何到达各个景点、推荐的交通方式、预计时间。"
    
    if query_type == 'strategy' or query_type == 'general':
        prompt += "\n请提供旅游策略建议，包括最佳游览时间、门票预订、必备物品、注意事项等。"
    
    if user_input:
        prompt += f"\n用户的特殊需求：{user_input}"
    
    prompt += "\n\n请用Markdown格式输出，包含清晰的标题和列表。"
    
    try:
        # 调用OpenAI API
        response = openai.ChatCompletion.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一个专业的旅游规划助手，擅长为游客制定详细的旅游计划。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        ai_response = response.choices[0].message.content
        
        # 解析AI响应（根据实际返回格式调整）
        result = self._parse_ai_response(ai_response, query_type)
        return result
        
    except Exception as e:
        # 如果AI API调用失败，回退到规则引擎
        print(f"OpenAI API调用失败: {e}")
        return self._generate_plan_fallback(scenic_spots, query_type, user_input)

def _parse_ai_response(self, ai_response, query_type):
    """
    解析AI返回的内容
    根据实际AI返回格式调整
    """
    result = {
        'route_plan': '',
        'transport_plan': '',
        'strategy_plan': ''
    }
    
    # 这里需要根据AI实际返回格式进行解析
    # 示例：如果AI返回的是Markdown格式，可以按章节分割
    if query_type in ['route', 'general']:
        # 提取路线规划部分
        result['route_plan'] = self._extract_section(ai_response, '路线')
    
    if query_type in ['transport', 'general']:
        # 提取交通规划部分
        result['transport_plan'] = self._extract_section(ai_response, '交通')
    
    if query_type in ['strategy', 'general']:
        # 提取旅游策略部分
        result['strategy_plan'] = self._extract_section(ai_response, '策略')
    
    return result

def _extract_section(self, text, keyword):
    """从文本中提取特定章节"""
    # 简单实现，可以根据实际需求优化
    lines = text.split('\n')
    section_lines = []
    in_section = False
    
    for line in lines:
        if keyword in line:
            in_section = True
        if in_section:
            section_lines.append(line)
            if line.startswith('##') and keyword not in line:
                break
    
    return '\n'.join(section_lines) if section_lines else text
```

### 方案2：集成百度文心一言

#### 1. 安装依赖

```bash
pip install qianfan
```

#### 2. 配置

在 `settings.py` 中：

```python
# 百度文心一言配置
QIANFAN_ACCESS_KEY = os.getenv('QIANFAN_ACCESS_KEY', '')
QIANFAN_SECRET_KEY = os.getenv('QIANFAN_SECRET_KEY', '')
```

#### 3. 修改代码

```python
import qianfan

def _generate_plan(self, scenic_spots, query_type, user_input):
    chat_comp = qianfan.ChatCompletion()
    
    prompt = f"请为以下景点规划旅游：{', '.join([s['name'] for s in scenic_spots])}"
    
    resp = chat_comp.do(
        model="ERNIE-Bot-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # 处理响应...
```

### 方案3：集成阿里通义千问

#### 1. 安装依赖

```bash
pip install dashscope
```

#### 2. 配置

```python
import dashscope
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY', '')
```

#### 3. 使用

```python
from dashscope import Generation

def _generate_plan(self, scenic_spots, query_type, user_input):
    prompt = f"请为以下景点规划旅游：{', '.join([s['name'] for s in scenic_spots])}"
    
    response = Generation.call(
        model='qwen-turbo',
        prompt=prompt
    )
    
    # 处理响应...
```

## 配置开关

为了支持在规则引擎和AI API之间切换，可以在 `settings.py` 中添加：

```python
# AI配置
USE_AI_API = True  # False时使用规则引擎
AI_PROVIDER = 'openai'  # 'openai', 'qianfan', 'dashscope'
```

然后在 `_generate_plan` 方法中：

```python
def _generate_plan(self, scenic_spots, query_type, user_input):
    if settings.USE_AI_API:
        return self._generate_plan_with_ai(scenic_spots, query_type, user_input)
    else:
        return self._generate_plan_with_rules(scenic_spots, query_type, user_input)
```

## 注意事项

1. **API密钥安全**：不要将API密钥提交到代码仓库，使用环境变量
2. **错误处理**：AI API可能失败，需要回退到规则引擎
3. **成本控制**：AI API调用有成本，建议添加缓存或限制调用频率
4. **响应格式**：不同AI服务返回格式不同，需要适配
5. **超时处理**：设置合理的超时时间，避免用户等待过久

## 测试

集成AI API后，建议：

1. 测试各种输入场景
2. 测试API失败时的回退机制
3. 监控API调用成本和频率
4. 收集用户反馈，优化提示词

## 示例：完整的OpenAI集成

参考 `apps/ai_assistant/api_openai_example.py`（如果创建了示例文件）

---

**提示**：当前版本使用规则引擎，功能完整且免费。如需更智能的规划，可以按照上述步骤集成真实的AI服务。

