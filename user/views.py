# user.views
import random

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView, CreateView

from new import settings
from new.settings import EMAIL_HOST_USER
from .forms import UserForm, UserRegisterForm
from .models import User


# Список пользователей
@login_required
@permission_required('user.view_user', raise_exception=True)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user/u_list.html', {'users': users})


# Детали пользователя
@login_required
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'user/u_detail.html', {'user': user})


# Создание пользователя
@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно создан.')
            return redirect('user:u_list')
    else:
        form = UserForm()
    return render(request, 'user/u_form.html', {'form': form})


# Редактирование пользователя
@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно отредактирован.')
            return redirect('user:u_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user/u_form.html', {'form': form})


# Удаление пользователя
@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'Пользователь успешно удален.')
    return redirect('user:user_list')


# Подтверждение почтового адреса пользователя
def activate_user(request):
    key = request.GET.get('token')
    print(key)
    current_user = User.objects.filter(is_verified=False, token=key)
    print(current_user)
    for user in current_user:
        user.is_verified = True
        user.token = None
        user.save()
    messages.success(request, 'Пользователь успешно верифицирован.')
    return redirect(reverse_lazy('user:u_login'))


# Выход пользователя
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли.')
    return redirect('user:u_login')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:u_login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_verified = False
        secret_token = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        new_user.token = secret_token
        new_user.save()
        message = (f'Вы указали этот E-mail в качестве основного адреса на нашей платформе!'
                   f'\nДля подтверждения вашего Е-mail перейдите по ссылке '
                   f'http://127.0.0.1:8000/user/verify/?token={secret_token}')
        send_mail(
            subject='Подтверждение E-mail адреса',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        messages.success(self.request, 'На ваш email отправлено письмо с инструкциями по верификации.')
        return super().form_valid(form)


class ResetPasswordView(FormView):
    form_class = PasswordResetForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('user:u_login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(self.request, 'Пользователь с таким email не найден.')
            return redirect('user:u_login')

        new_password = User.objects.make_random_password()
        user.set_password(new_password)
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_password_link = f'http://{self.request.get_host()}/reset_password/{uid}/{token}/'
        send_mail(
            'Сброс пароля',
            f'Ваш новый пароль: {new_password}. Или перейдите по ссылке для установки '
            f'нового пароля: {reset_password_link}',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(self.request, 'На ваш email отправлено письмо с инструкциями по сбросу пароля.')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('user:u_login')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменен. Войдите с новым паролем.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Ссылка для сброса пароля недействительна.')
        return super().form_invalid(form)
