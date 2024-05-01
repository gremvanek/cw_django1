# user.forms
from django import forms
from django.contrib.auth import get_user_model

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Подтверждение пароля', strip=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'avatar', 'country']

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
            raise forms.ValidationError('Пароли не совпадают.')
        return password1


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'avatar', 'country', 'is_verified', 'have_permissions']


class CustomPasswordResetForm(forms.Form):
    User = get_user_model()
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email не найден.')
        return email


class VerificationCodeResetForm(forms.Form):
    email = forms.EmailField(label='Email')
