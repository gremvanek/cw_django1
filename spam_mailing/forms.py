from django import forms

from .models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'last_name', 'first_name', 'middle_name', 'comment']
        labels = {
            'email': 'Email',
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'comment': 'Комментарий',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['client', 'send_time', 'frequency', 'status']
        labels = {
            'client': 'Клиенты',
            'send_time': 'Время отправки',
            'frequency': 'Рассылка',
            'status': 'Статус',
        }
        widgets = {
            'client': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'send_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['mailing', 'subject', 'body']
        labels = {
            'mailing': 'Рассылка',
            'subject': 'Тема письма',
            'body': 'Содержание письма',
        }
        widgets = {
            'mailing': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
