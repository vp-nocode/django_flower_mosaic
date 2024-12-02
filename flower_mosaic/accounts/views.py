from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserRegisterForm, CustomUserLoginForm


def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            clients_group, created = Group.objects.get_or_create(name='Clients')
            user.groups.add(clients_group)

            if user is not None:
                login(request, user)
                messages.success(request, "Регистрация успешно завершена!")
                return redirect('catalog')
    else:
        form = CustomUserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    form = CustomUserLoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalog')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('catalog')
