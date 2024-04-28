from django import forms
from .models import Client


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
