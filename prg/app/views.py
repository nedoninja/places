# app/views.py

import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .models import Profile

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        # собираем данные
        data = {
            'username': request.POST.get('username', '').strip(),
            'password': request.POST.get('password', ''),
            'password_confirm': request.POST.get('password_confirm', ''),
            'email': request.POST.get('email', '').strip(),
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'middle_name': request.POST.get('middle_name', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'city': request.POST.get('city', '').strip(),
            'birth_date': request.POST.get('birth_date', ''),
            'role': request.POST.get('role', ''),
        }

        errors = []
        if User.objects.filter(username=data['username']).exists():
            errors.append('Пользователь с таким логином уже существует')
        if User.objects.filter(email=data['email']).exists():
            errors.append('Пользователь с таким email уже существует')
        if data['password'] != data['password_confirm']:
            errors.append('Пароли не совпадают')
        try:
            validate_email(data['email'])
        except ValidationError:
            errors.append('Введите корректный email')

        if errors:
            for err in errors:
                messages.error(request, err)
            # рендерим заново с отображением сообщений
            return render(request, 'register.html', context=data)

        try:
            # создаём неактивного пользователя
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            user.is_active = False
            user.save()

            Profile.objects.create(
                user=user,
                middle_name=data['middle_name'],
                phone=data['phone'],
                city=data['city'],
                birth_date=data['birth_date'],
                role=data['role']
            )

            # генерируем токен и ссылку
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(f"/activate/{uid}/{token}/")

            subject = 'Подтвердите вашу почту'
            message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            try:
                send_mail(subject, message, None, [data['email']], fail_silently=False)
            except BadHeaderError as e:
                logger.error("Ошибка отправки письма активации: %s", e)
                messages.error(request, 'Не удалось отправить письмо. Попробуйте позже.')
                return render(request, 'register.html', context=data)

            messages.success(request,
                'Письмо для подтверждения отправлено. '
                'Пожалуйста, проверьте почту и перейдите по ссылке.'
            )
            return redirect('login')

        except Exception as e:
            logger.exception("Ошибка при создании пользователя:")
            messages.error(request, f'Не удалось зарегистрировать: {e}')
            return render(request, 'register.html', context=data)

    # GET-запрос — просто пустая форма
    return render(request, 'register.html')
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email подтверждён. Теперь можно войти.')
        return redirect('login')
    else:
        return HttpResponse('Ссылка недействительна или уже использована.', status=400)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Аккаунт не активирован. Проверьте почту.')
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