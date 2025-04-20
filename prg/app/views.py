from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, Service, Feedback, Transaction, Wallet
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, Service
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
from django.http import HttpResponse
from .models import Profile
from decimal import Decimal, InvalidOperation


def is_executor(user):
    return user.profile.role == 'executor'

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username'].strip()
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            email = request.POST['email'].strip()
            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()
            middle_name = request.POST.get('middle_name', '').strip()
            phone = request.POST['phone'].strip()
            city = request.POST['city'].strip()
            birth_date = request.POST['birth_date']
            role = request.POST['role']
        except KeyError as e:
            messages.error(request, f'Отсутствует поле: {e}')
            return render(request, 'register.html')

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
            for err in errors:
                messages.error(request, err)
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'middle_name': middle_name,
                'phone': phone,
                'city': city,
                'birth_date': birth_date,
                'role': role
            })

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.is_active = False
            user.save()

            Profile.objects.create(
                user=user,
                middle_name=middle_name,
                phone=phone,
                city=city,
                birth_date=birth_date,
                role=role
            )

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                f"/activate/{uid}/{token}/"
            )

            subject = 'Подтвердите вашу почту'
            message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(subject, message, None, [email], fail_silently=False)

            return redirect('check_mail')

        except Exception as e:
            #logger.exception("Ошибка при создании пользователя:")
            messages.error(request, f'Не удалось зарегистрировать: {e}')
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'middle_name': middle_name,
                'phone': phone,
                'city': city,
                'birth_date': birth_date,
                'role': role
            })

    return render(request, 'register.html')


def check_mail(request):
    return render(request, 'check_your_gmail.html')
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
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'services': services})


def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'service_detail.html', {'service': service})


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

@login_required
@user_passes_test(is_executor)
def create_service(request):
    if request.method == 'POST':
        service = Service(
            author=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            price=request.POST['price'],
            image=request.FILES['image']
        )
        service.save()
        return redirect('home')
    return render(request, 'create_service.html')


@login_required
def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    user_profile = request.user.profile 
    is_customer = user_profile.role == 'customer'
    feedback_submitted = False  

    if request.method == 'POST':
        if is_customer:
            feedback_text = request.POST.get('feedback_text')
            if feedback_text:
                Feedback.objects.create(service=service, author=request.user, text=feedback_text)
                messages.success(request, 'Отзыв успешно отправлен!')
                feedback_submitted = True 
                return redirect('service_detail', service_id=service_id) 

    return render(request, 'service_detail.html', {
        'service': service,
        'is_customer': is_customer,
        'feedback_submitted': feedback_submitted 
    })


@login_required
def my_feedbacks(request):
    if request.user.profile.role == 'executor':
        feedbacks = Feedback.objects.filter(service__author=request.user)  
        return render(request, 'my_feedbacks.html', {'feedbacks': feedbacks})
    else:
        messages.error(request, "У вас нет прав для просмотра этой страницы.")
        return redirect('home')

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
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'service_detail.html', {'service': service})


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

@login_required
@user_passes_test(is_executor)
def create_service(request):
    if request.method == 'POST':
        service = Service(
            author=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            price=request.POST['price'],
            image=request.FILES['image']
        )
        service.save()
        return redirect('home')
    return render(request, 'create_service.html')


@login_required
def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    user_profile = request.user.profile  
    is_customer = user_profile.role == 'customer'
    feedback_submitted = False  

    if request.method == 'POST':
        if is_customer:
            feedback_text = request.POST.get('feedback_text')
            if feedback_text:
                Feedback.objects.create(service=service, author=request.user, text=feedback_text)
                messages.success(request, 'Отзыв успешно отправлен!')
                feedback_submitted = True 
                return redirect('service_detail', service_id=service_id) 

    return render(request, 'service_detail.html', {
        'service': service,
        'is_customer': is_customer,
        'feedback_submitted': feedback_submitted 
    })


@login_required
def my_feedbacks(request):
    if request.user.profile.role == 'executor':
        feedbacks = Feedback.objects.filter(service__author=request.user) 
        return render(request, 'my_feedbacks.html', {'feedbacks': feedbacks})
    else:
        messages.error(request, "У вас нет прав для просмотра этой страницы.")
        return redirect('home')


from decimal import Decimal
from django.db import transaction


@login_required
def add_balance(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")

            with transaction.atomic():
                wallet, created = Wallet.objects.get_or_create(user=request.user)
                wallet.balance += amount
                wallet.save()

                Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type='deposit',
                    description=f"Пополнение баланса"
                )

            messages.success(request, f'Баланс пополнен на {amount} ₽')
            return redirect('profile')

        except (ValueError, InvalidOperation) as e:
            messages.error(request, f'Ошибка: {str(e)}')

    return render(request, 'add_balance.html')


@login_required
def process_payment(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    user_profile = request.user.profile

    if user_profile.role != 'customer':
        messages.error(request, "Только заказчики могут оплачивать услуги")
        return redirect('service_detail', service_id=service_id)

    with transaction.atomic():
        customer_wallet = request.user.wallet
        executor_wallet = service.author.wallet

        if customer_wallet.balance < service.price:
            messages.error(request, "Недостаточно средств на балансе")
            return redirect('service_detail', service_id=service_id)

        # Списание у заказчика
        customer_wallet.balance -= service.price
        customer_wallet.save()

        Transaction.objects.create(
            user=request.user,
            amount=-service.price,
            transaction_type='payment',
            description=f"Оплата услуги '{service.title}'"
        )

        # Зачисление исполнителю
        executor_wallet.balance += service.price
        executor_wallet.save()

        Transaction.objects.create(
            user=service.author,
            amount=service.price,
            transaction_type='income',
            description=f"Получение оплаты за услугу '{service.title}'"
        )

    messages.success(request, "Оплата прошла успешно!")
    return redirect('service_detail', service_id=service_id)