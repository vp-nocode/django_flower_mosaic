from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import TextInput, EmailInput, PasswordInput
from .models import CustomUser

class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя заказчика'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес доставки'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
