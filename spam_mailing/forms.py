from django import forms

from .models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ClientForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.owner = user

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
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields.pop('status', None)  # удаляем поле status для обычных пользователей

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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.owner = user

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
