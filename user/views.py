import secrets
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import UserRegistrationForm, UserForm
from .models import User


# Список пользователей
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user/u_list.html', {'users': users})


# Детали пользователя
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'user/u_detail.html', {'user': user})


# Создание пользователя
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно создан.')
            return redirect('user:user_list')
    else:
        form = UserForm()
    return render(request, 'user/u_form.html', {'form': form})


# Редактирование пользователя
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно отредактирован.')
            return redirect('user:user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user/u_form.html', {'form': form})


# Удаление пользователя
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'Пользователь успешно удален.')
    return redirect('user:user_list')


# Подтверждение почтового адреса пользователя
class VerifyEmailView(View):
    @staticmethod
    def get(request):
        verification_code = request.GET.get('code')
        try:
            user = User.objects.get(verification_code=verification_code)
            user.is_verified = True
            user.save()
            messages.success(request, 'Адрес электронной почты успешно подтвержден.')
            return redirect('user:u_login')
        except User.DoesNotExist:
            messages.error(request, 'Неверный код подтверждения.')
            return render(request, 'user/verification_error.html', {'verification_code': verification_code})


# # Вход пользователя
# class UserLoginView(View):
#     @staticmethod
#     def get(request):
#         form = UserLoginForm()
#         return render(request, 'user/u_login.html', {'form': form})
#
#     @staticmethod
#     def post(request):
#         form = UserLoginForm(request.POST)
#         password = request.POST.get('password')  # Получаем пароль до проверки на валидность
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             try:
#                 user = User.objects.get(email=email)
#                 if check_password(password, user.password):
#                     login(request, user)
#                     messages.success(request, 'Вы успешно вошли.')
#                     return redirect('spam_mailing:client_list')
#             except User.DoesNotExist:
#                 pass
#         messages.error(request, 'Неправильный email или пароль.')
#         return render(request, 'user/u_login.html', {'form': form})


# Выход пользователя
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли.')
    return redirect('user:u_login')


def generate_verification_code(length=6):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class UserRegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'user/u_register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.is_verified = False
            user.save()

            verification_code = generate_verification_code()
            user.verification_code = verification_code
            user.save()

            send_verification_email(user.email, verification_code, user.username)

            messages.success(request,
                             'Пользователь успешно зарегистрирован. '
                             'Пожалуйста, проверьте вашу почту для завершения регистрации.')
            return redirect('user:u_login')
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, проверьте данные.')
            return render(request, 'user/u_register.html', {'form': form})


def send_verification_email(email, verification_code, username):
    subject = 'Подтверждение адреса электронной почты'
    message = f'Привет, {username}!\n' \
              f'Перейдите по ссылке ниже, чтобы подтвердить ваш адрес электронной почты:\n' \
              f'http://127.0.0.1:8000/verify-email/?code={verification_code}\n' \
              f'С уважением,\n' \
              f'Ваша команда'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
