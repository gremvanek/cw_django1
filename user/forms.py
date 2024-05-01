# user.forms
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


# class UserLoginForm(AuthenticationForm):
#     username = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Подтверждение пароля', strip=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'avatar', 'country']

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
