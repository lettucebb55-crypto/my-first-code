import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from apps.scenic.models import ScenicSpot
from apps.routes.models import Route
from .models import AIQuery


@method_decorator(csrf_exempt, name='dispatch')
class AIPlanAPIView(View):
    """
    AI助手规划API
    根据用户输入的景点，生成路线规划、交通规划、旅游策略
    """
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            scenic_spot_names = data.get('scenic_spots', [])  # 景点名称列表
            query_type = data.get('query_type', 'general')  # route, transport, strategy, general
            user_input = data.get('user_input', '')  # 用户额外输入
            
            if not scenic_spot_names:
                return JsonResponse({
                    'status': 'error',
                    'message': '请至少输入一个景点'
                }, status=400)
            
            # 查询景点信息
            scenic_spots = []
            not_found_spots = []  # 记录未找到的景点
            
            for name in scenic_spot_names:
                name = name.strip()  # 去除首尾空格
                if not name:
                    continue
                    
                # 尝试多种匹配方式
                spot = None
                # 1. 精确匹配
                spot = ScenicSpot.objects.filter(name=name).first()
                # 2. 包含匹配
                if not spot:
                    spot = ScenicSpot.objects.filter(name__icontains=name).first()
                # 3. 如果还是找不到，尝试去掉常见后缀后匹配
                if not spot:
                    # 去掉可能的"景区"、"公园"等后缀
                    name_variants = [
                        name.replace('景区', '').replace('公园', '').replace('景点', '').strip(),
                        name.replace('旅游区', '').replace('风景区', '').strip(),
                    ]
                    for variant in name_variants:
                        if variant and variant != name:
                            spot = ScenicSpot.objects.filter(name__icontains=variant).first()
                            if spot:
                                break
                
                if spot:
                    scenic_spots.append({
                        'id': spot.id,
                        'name': spot.name,
                        'address': spot.address,
                        'ticket_price': str(spot.ticket_price),
                        'open_time': spot.open_time,
                        'description': spot.description[:200],
                        'latitude': float(spot.latitude) if spot.latitude else None,
                        'longitude': float(spot.longitude) if spot.longitude else None,
                    })
                else:
                    not_found_spots.append(name)
            
            # 如果所有景点都没找到，返回错误
            if not scenic_spots:
                error_msg = '未找到匹配的景点，请检查景点名称。'
                if not_found_spots:
                    error_msg += f'\n未找到的景点：{", ".join(not_found_spots)}'
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=404)
            
            # 如果部分景点没找到，在响应中提示
            warning_message = None
            if not_found_spots:
                warning_message = f'以下景点未找到：{", ".join(not_found_spots)}，将基于已找到的景点生成规划。'
            
            # 生成AI规划（这里使用规则引擎，后续可以替换为真实AI）
            plan_result = self._generate_plan(scenic_spots, query_type, user_input)
            
            # 保存查询记录（如果用户已登录）
            ai_query = None
            if request.user.is_authenticated:
                ai_query = AIQuery.objects.create(
                    user=request.user,
                    query_type=query_type,
                    scenic_spots=json.dumps(scenic_spots, ensure_ascii=False),
                    user_input=user_input or f"规划{', '.join(scenic_spot_names)}的旅游",
                    route_plan=plan_result.get('route_plan', ''),
                    transport_plan=plan_result.get('transport_plan', ''),
                    strategy_plan=plan_result.get('strategy_plan', ''),
                    full_response=json.dumps(plan_result, ensure_ascii=False)
                )
            
            response_data = {
                'scenic_spots': scenic_spots,
                'plan': plan_result,
                'query_id': ai_query.id if ai_query else None,
                'is_favorite': ai_query.is_favorite if ai_query else False
            }
            
            # 如果有警告信息，添加到响应中
            if warning_message:
                response_data['warning'] = warning_message
            
            return JsonResponse({
                'status': 'success',
                'data': response_data
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': '请求数据格式错误'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'服务器错误: {str(e)}'
            }, status=500)
    
    def _generate_plan(self, scenic_spots, query_type, user_input):
        """
        生成旅游规划
        这里使用规则引擎生成基础规划，后续可以替换为真实AI服务
        """
        result = {
            'route_plan': '',
            'transport_plan': '',
            'strategy_plan': ''
        }
        
        # 路线规划
        if query_type in ['route', 'general']:
            route_plan = self._generate_route_plan(scenic_spots, user_input)
            result['route_plan'] = route_plan
        
        # 交通规划
        if query_type in ['transport', 'general']:
            transport_plan = self._generate_transport_plan(scenic_spots)
            result['transport_plan'] = transport_plan
        
        # 旅游策略
        if query_type in ['strategy', 'general']:
            strategy_plan = self._generate_strategy_plan(scenic_spots, user_input)
            result['strategy_plan'] = strategy_plan
        
        return result
    
    def _generate_route_plan(self, scenic_spots, user_input=''):
        """生成路线规划"""
        # 解析用户输入，识别时间需求
        user_input_lower = (user_input or '').lower()
        days_requested = None
        
        # 识别天数需求
        if '一天' in user_input_lower or '1天' in user_input_lower or '一日' in user_input_lower or '一天完成' in user_input_lower:
            days_requested = 1
        elif '两天' in user_input_lower or '2天' in user_input_lower or '二日' in user_input_lower:
            days_requested = 2
        elif '三天' in user_input_lower or '3天' in user_input_lower or '三日' in user_input_lower:
            days_requested = 3
        
        # 如果只有一个景点，直接生成一日游
        if len(scenic_spots) == 1:
            spot = scenic_spots[0]
            return f"""
## 一日游路线规划

### 景点：{spot['name']}

**推荐行程：**
- **上午（9:00-12:00）**：抵达{spot['name']}，参观主要景点，了解历史文化背景
- **中午（12:00-13:30）**：在景区内或附近用餐，品尝当地特色美食
- **下午（13:30-17:00）**：继续游览，体验特色项目，拍照留念
- **傍晚（17:00-18:00）**：结束游览，返回

**门票信息：** ¥{spot['ticket_price']}
**开放时间：** {spot['open_time']}
**建议游览时长：** 3-4小时
"""
        # 多个景点的情况
        else:
            # 如果用户要求一天完成，将所有景点安排在同一天
            if days_requested == 1:
                plan = "## 一日游路线规划\n\n"
                plan += "**行程安排：**\n\n"
                
                for i, spot in enumerate(scenic_spots, 1):
                    if i == 1:
                        plan += f"""
### 上午：{spot['name']}

- **时间**：9:00-12:00
- **地址**：{spot['address']}
- **游览重点**：{spot['description'][:80]}...
- **门票价格**：¥{spot['ticket_price']}
- **开放时间**：{spot['open_time']}

"""
                    elif i == 2:
                        plan += f"""
### 中午：用餐休息

- **时间**：12:00-13:30
- 建议在{scenic_spots[0]['name']}附近用餐，然后前往下一景点

"""
                        plan += f"""
### 下午：{spot['name']}

- **时间**：13:30-17:00
- **地址**：{spot['address']}
- **游览重点**：{spot['description'][:80]}...
- **门票价格**：¥{spot['ticket_price']}
- **开放时间**：{spot['open_time']}

"""
                    else:
                        plan += f"""
### 傍晚：{spot['name']}

- **时间**：17:00-18:30
- **地址**：{spot['address']}
- **游览重点**：{spot['description'][:80]}...
- **门票价格**：¥{spot['ticket_price']}
- **开放时间**：{spot['open_time']}

"""
                
                plan += "\n**温馨提示：**\n"
                plan += "- 行程较为紧凑，建议提前规划好交通路线\n"
                plan += "- 建议提前预订门票，节省排队时间\n"
                plan += "- 如果时间紧张，可以选择重点游览部分景点\n"
                plan += "- 注意各景点的开放时间，合理安排行程\n"
                return plan
            else:
                # 默认多日游，每个景点一天
                plan = "## 多日游路线规划\n\n"
                for i, spot in enumerate(scenic_spots, 1):
                    plan += f"""
### 第{i}天：{spot['name']}

**行程安排：**
- **上午**：前往{spot['name']}（地址：{spot['address']}）
- **游览重点**：{spot['description'][:100]}...
- **门票价格**：¥{spot['ticket_price']}
- **开放时间**：{spot['open_time']}
- **建议游览时长**：半天

"""
                plan += "\n**温馨提示：**\n"
                plan += "- 建议提前预订门票，避免排队\n"
                plan += "- 根据景点距离合理安排交通方式\n"
                plan += "- 预留充足的游览时间，不要过于匆忙\n"
                return plan
    
    def _generate_transport_plan(self, scenic_spots):
        """生成交通规划"""
        plan = "## 交通规划\n\n"
        
        if len(scenic_spots) == 1:
            spot = scenic_spots[0]
            plan += f"""
### 前往{spot['name']}

**推荐交通方式：**

1. **自驾游**
   - 从保定市区出发，使用导航软件搜索"{spot['name']}"
   - 预计车程：根据距离而定
   - 停车建议：景区通常有停车场，建议提前了解停车费用

2. **公共交通**
   - 可查询保定市公交线路或旅游专线
   - 建议使用高德地图或百度地图查询具体路线
   - 部分景点可能需要转乘

3. **包车/租车**
   - 适合多人出行，更加灵活便捷
   - 可以提前联系当地旅行社或租车公司

**地址：** {spot['address']}
"""
        else:
            plan += "### 多景点交通规划\n\n"
            for i, spot in enumerate(scenic_spots, 1):
                plan += f"""
**第{i}站：{spot['name']}**
- 地址：{spot['address']}
- 建议交通：根据距离选择自驾或公共交通
"""
            
            plan += "\n**交通建议：**\n"
            plan += "- 如果景点距离较近（<20公里），建议自驾或包车，更加灵活\n"
            plan += "- 如果景点距离较远，可以考虑公共交通，但需要提前规划好路线和时间\n"
            plan += "- 建议使用导航软件实时查看路况，避开拥堵路段\n"
        
        return plan
    
    def _generate_strategy_plan(self, scenic_spots, user_input):
        """生成旅游策略"""
        plan = "## 旅游策略建议\n\n"
        
        plan += "### 游览建议\n\n"
        plan += f"根据您选择的{len(scenic_spots)}个景点，为您提供以下旅游策略：\n\n"
        
        plan += "**1. 时间安排**\n"
        if len(scenic_spots) == 1:
            plan += "- 建议安排1天时间，充分游览\n"
        else:
            plan += f"- 建议安排{len(scenic_spots)}-{len(scenic_spots)+1}天时间，每天游览1-2个景点\n"
            plan += "- 避免行程过于紧张，留出休息时间\n"
        
        plan += "\n**2. 门票预订**\n"
        total_price = sum(float(spot['ticket_price']) for spot in scenic_spots)
        plan += f"- 预计总门票费用：¥{total_price:.2f}\n"
        plan += "- 建议提前在线预订，享受优惠价格\n"
        plan += "- 部分景点可能有学生票、老年票等优惠政策\n"
        
        plan += "\n**3. 最佳游览时间**\n"
        plan += "- 建议选择非节假日出行，避免人流高峰\n"
        plan += "- 春秋季节气候宜人，是最佳游览时间\n"
        plan += "- 夏季注意防暑，冬季注意保暖\n"
        
        plan += "\n**4. 必备物品**\n"
        plan += "- 身份证、学生证等有效证件\n"
        plan += "- 舒适的鞋子和衣物\n"
        plan += "- 相机或手机（记录美好瞬间）\n"
        plan += "- 充电宝、雨具等\n"
        
        plan += "\n**5. 注意事项**\n"
        plan += "- 遵守景区规定，保护环境\n"
        plan += "- 注意人身和财产安全\n"
        plan += "- 提前了解景点的开放时间和特殊规定\n"
        
        if user_input:
            plan += f"\n**6. 特别提醒**\n"
            plan += f"- {user_input}\n"
        
        return plan


@method_decorator(csrf_exempt, name='dispatch')
class AIQueryHistoryAPIView(LoginRequiredMixin, View):
    """
    获取用户的AI查询历史
    """
    
    def get(self, request):
        queries = AIQuery.objects.filter(user=request.user).order_by('-created_at')[:20]
        
        data = []
        for query in queries:
            data.append({
                'id': query.id,
                'query_type': query.query_type,
                'query_type_display': query.get_query_type_display(),
                'user_input': query.user_input,
                'created_at': query.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_favorite': query.is_favorite
            })
        
        return JsonResponse({
            'status': 'success',
            'data': data
        })


@method_decorator(csrf_exempt, name='dispatch')
class AIQueryDetailAPIView(LoginRequiredMixin, View):
    """
    获取AI查询详情
    """
    
    def get(self, request, query_id):
        try:
            query = AIQuery.objects.get(id=query_id, user=request.user)
            
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': query.id,
                    'query_type': query.query_type,
                    'query_type_display': query.get_query_type_display(),
                    'user_input': query.user_input,
                    'scenic_spots': json.loads(query.scenic_spots),
                    'route_plan': query.route_plan,
                    'transport_plan': query.transport_plan,
                    'strategy_plan': query.strategy_plan,
                    'created_at': query.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_favorite': query.is_favorite
                }
            })
        except AIQuery.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': '查询记录不存在'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AIQueryFavoriteAPIView(LoginRequiredMixin, View):
    """
    收藏/取消收藏AI规划结果
    """
    
    def post(self, request, query_id):
        """收藏规划结果"""
        try:
            query = AIQuery.objects.get(id=query_id, user=request.user)
            query.is_favorite = True
            query.save()
            
            return JsonResponse({
                'status': 'success',
                'message': '收藏成功',
                'is_favorite': True
            })
        except AIQuery.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': '查询记录不存在'
            }, status=404)
    
    def delete(self, request, query_id):
        """取消收藏"""
        try:
            query = AIQuery.objects.get(id=query_id, user=request.user)
            query.is_favorite = False
            query.save()
            
            return JsonResponse({
                'status': 'success',
                'message': '取消收藏成功',
                'is_favorite': False
            })
        except AIQuery.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': '查询记录不存在'
            }, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AIQueryExportAPIView(LoginRequiredMixin, View):
    """
    导出AI规划结果为文本
    """
    
    def get(self, request, query_id):
        try:
            query = AIQuery.objects.get(id=query_id, user=request.user)
            scenic_spots = json.loads(query.scenic_spots)
            
            # 构建导出文本
            export_text = f"""
{'='*60}
保定旅游网 - AI智能规划结果
{'='*60}

查询时间：{query.created_at.strftime('%Y年%m月%d日 %H:%M:%S')}
规划类型：{query.get_query_type_display()}
用户需求：{query.user_input}

{'='*60}
景点信息
{'='*60}
"""
            for i, spot in enumerate(scenic_spots, 1):
                export_text += f"""
{i}. {spot['name']}
   地址：{spot['address']}
   门票：¥{spot['ticket_price']}
   开放时间：{spot['open_time']}
"""
            
            if query.route_plan:
                export_text += f"""
{'='*60}
路线规划
{'='*60}
{query.route_plan}
"""
            
            if query.transport_plan:
                export_text += f"""
{'='*60}
交通规划
{'='*60}
{query.transport_plan}
"""
            
            if query.strategy_plan:
                export_text += f"""
{'='*60}
旅游策略
{'='*60}
{query.strategy_plan}
"""
            
            export_text += f"""
{'='*60}
感谢使用保定旅游网AI助手！
{'='*60}
"""
            
            from django.http import HttpResponse
            response = HttpResponse(export_text, content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="ai_plan_{query_id}.txt"'
            return response
            
        except AIQuery.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': '查询记录不存在'
            }, status=404)

