from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Food, FoodCategory


class FoodListView(ListView):
    """美食列表页"""
    model = Food
    template_name = 'foods/list.html'
    context_object_name = 'foods'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Food.objects.select_related('category').prefetch_related('images').all()
        
        # 分类筛选
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 搜索
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(ingredients__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # 筛选条件
        is_hot = self.request.GET.get('is_hot')
        if is_hot == '1':
            queryset = queryset.filter(is_hot=True)
        
        is_traditional = self.request.GET.get('is_traditional')
        if is_traditional == '1':
            queryset = queryset.filter(is_traditional=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FoodCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['search'] = self.request.GET.get('search', '')
        context['is_hot'] = self.request.GET.get('is_hot')
        context['is_traditional'] = self.request.GET.get('is_traditional')
        return context


class FoodDetailView(DetailView):
    """美食详情页"""
    model = Food
    template_name = 'foods/detail.html'
    context_object_name = 'food'
    
    def get_queryset(self):
        return Food.objects.select_related('category').prefetch_related('images')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # 增加浏览次数
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取相关美食（同分类的其他美食）
        if self.object.category:
            context['related_foods'] = Food.objects.filter(
                category=self.object.category
            ).exclude(id=self.object.id)[:6]
        else:
            context['related_foods'] = Food.objects.exclude(id=self.object.id)[:6]
        return context
