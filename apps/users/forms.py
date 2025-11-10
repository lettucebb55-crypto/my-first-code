from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # 让用户在注册时填写手机号
        fields = UserCreationForm.Meta.fields + ('phone', 'avatar')