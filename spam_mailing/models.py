# spam_mailing.models.py
from django.db import models
from django.utils import timezone

from user.models import User


class Client(models.Model):
    objects = models.Manager()
    email = models.EmailField(verbose_name="Email")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name="Активен")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="clients")

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        return full_name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Mailing(models.Model):

    class Meta:
        permissions = [
            ("can_view_mailing", "Can view mailing"),
            ("can_stop_mailing", "Can stop mailing"),
        ]

    client = models.ManyToManyField(Client, verbose_name="Клиенты")
    send_time = models.DateTimeField(default=timezone.now, verbose_name="Время отправки")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="mailings")
    frequency_choices = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]
    frequency = models.CharField(max_length=10, choices=frequency_choices, verbose_name="Рассылка")

    status_choices = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
        ('stopped', 'Остановлена'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, verbose_name="Статус")

    def __str__(self):
        return f"Рассылка № {self.pk}"


class Message(models.Model):
    mailing = models.OneToOneField(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="message", unique=True)
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Содержание письма")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="messages")


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="logs")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время последней попытки")
    status = models.CharField(max_length=10, verbose_name="Статус попытки")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
