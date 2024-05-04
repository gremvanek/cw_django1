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
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        user = None
        if self.request:
            user = self.request.user
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields.pop('status', None)  # Remove the status field for regular users

    class Meta:
        model = Mailing
        fields = ['name', 'clients', 'start_time', 'period', 'status']
        labels = {
            'name': 'Название рассылки',
            'clients': 'Клиенты',
            'start_time': 'Время отправки',
            'period': 'Рассылка',
            'status': 'Статус',
            'message': 'Сообщение',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'period': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user and self.instance:
            self.instance.owner = user

    class Meta:
        model = Message
        fields = ['subject', 'body']
        labels = {
            'subject': 'Тема письма',
            'body': 'Содержание письма',
        }
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
