from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST.get('middle_name', '')
        phone = request.POST['phone']
        city = request.POST['city']
        birth_date = request.POST['birth_date']
        role = request.POST['role']

        errors = []
        
        if User.objects.filter(username=username).exists():
            errors.append('Пользователь с таким логином уже существует')
        
        if User.objects.filter(email=email).exists():
            errors.append('Пользователь с таким email уже существует')
        
        if password != password_confirm:
            errors.append('Пароли не совпадают')
        
        try:
            validate_email(email)
        except ValidationError:
            errors.append('Введите корректный email')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('register')

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            
            Profile.objects.create(
                user=user,
                middle_name=middle_name,
                phone=phone,
                city=city,
                birth_date=birth_date,
                role=role
            )
            
            login(request, user)
            return redirect('home')
        
        except Exception as e:
            messages.error(request, f'Ошибка при регистрации: {str(e)}')
            return redirect('register')
    
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
    user = request.user
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        user_profile = None
    
    context = {
        'user': user,
        'profile': user_profile,
        'date_joined': user.date_joined,
    }
    return render(request, 'profile.html', context)