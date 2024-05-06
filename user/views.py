# user.views
import secrets
import string
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, CreateView

from new.settings import EMAIL_HOST_USER
from .forms import UserForm, UserRegisterForm
from .models import User
from .utils import send_email_for_verify


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
class EmailVerifyView(View):
    success_url = reverse_lazy('user:u_login')

    @staticmethod
    def get(request, uidb64, token):
        try:
            # Decode uid and get the user
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Check token and user
        if user is not None and token_generator.check_token(user, token):
            # Set email_verified to True
            user.email_verified = True
            user.save()
            messages.success(request, "Your email has been successfully verified")
            return redirect('user:email_success')

        # If the token is invalid, show an error message
        messages.error(request, "The verification link is invalid or has expired")
        return redirect('user:email_fail')


# Выход пользователя
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли.')
    return redirect('user:u_login')


def generate_verification_code(length=6):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/u_register.html'
    success_url = reverse_lazy('user:u_login')

    def form_valid(self, form):
        # Сохраняем объект пользователя
        user = form.save(commit=False)
        user.save()

        # Отправляем письмо для подтверждения адреса электронной почты
        send_email_for_verify(self.request, user)

        # Перенаправляем пользователя на страницу входа
        return redirect(self.success_url)


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
