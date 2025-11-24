from django import forms
from apps.scenic.models import ScenicSpot, ScenicCategory
from apps.routes.models import Route, RouteCategory
from apps.hotels.models import Hotel
from apps.news.models import News, NewsCategory
from apps.users.models import CustomUser
from apps.orders.models import Order


class ScenicSpotForm(forms.ModelForm):
    class Meta:
        model = ScenicSpot
        fields = [
            'category', 'name', 'address', 'ticket_price', 'open_time', 'description',
            'cover_image', 'is_hot', 'is_recommended', 'rating', 'phone', 'traffic_info',
            'best_season', 'visit_duration', 'tags', 'latitude', 'longitude', 'display_order'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'open_time': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_hot': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_recommended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'traffic_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'best_season': forms.TextInput(attrs={'class': 'form-control'}),
            'visit_duration': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用逗号分隔，如：历史,文化,古迹'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = [
            'category', 'name', 'price', 'days', 'group_size', 'deadline',
            'cover_image', 'itinerary_summary', 'cost_include', 'cost_exclude', 'notes',
            'is_hot', 'is_recommended', 'departure_city', 'meeting_point', 'tags',
            'rating', 'display_order'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'days': forms.NumberInput(attrs={'class': 'form-control'}),
            'group_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'itinerary_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cost_include': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost_exclude': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_hot': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_recommended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'departure_city': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_point': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用逗号分隔'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'name', 'address', 'phone', 'brief', 'description', 'cover_image',
            'is_recommended', 'rating', 'latitude', 'longitude', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'brief': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_recommended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'category', 'title', 'abstract', 'content', 'cover_image', 'author'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只显示staff用户作为作者选项
        self.fields['author'].queryset = CustomUser.objects.filter(is_staff=True)
        if not self.instance.pk:  # 新建时，默认作者为当前用户
            self.fields['author'].initial = None


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='留空则不修改密码'
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'phone', 'avatar', 'is_staff', 'is_active', 'first_name', 'last_name'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

