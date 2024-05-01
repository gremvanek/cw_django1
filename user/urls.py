# user.urls
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView
from django.urls import path

from user.views import user_create, user_update, user_delete, VerifyEmailView, user_logout, user_list, user_detail, \
    UserRegisterView, CustomPasswordResetConfirmView

app_name = 'user'  # Пространство имен для приложения

urlpatterns = [
    path('users/', user_list, name='u_list'),
    path('user/<int:pk>/', user_detail, name='u_detail'),
    path('user/create/', user_create, name='u_create'),
    path('user/<int:pk>/update/', user_update, name='u_update'),
    path('user/<int:pk>/delete/', user_delete, name='u_delete'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('', LoginView.as_view(template_name='user/u_login.html'), name='u_login'),  # Главная страница
    path('logout/', user_logout, name='u_logout'),
    path('register/', UserRegisterView.as_view(), name='u_register'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
