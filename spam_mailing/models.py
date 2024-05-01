# spam.mailing.py
from django.db import models
from django.utils import timezone

from user.models import User


class Client(models.Model):
    objects = models.Manager()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", default=None)
    email = models.EmailField(verbose_name="Email")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}, {self.middle_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def make_active(self):
        self.is_active = True
        self.save()

    def inactive(self):
        self.is_active = False
        self.save()


class Mailing(models.Model):
    class Meta:
        permissions = [
            ("disable_mailing", "Can disable mailing"),
        ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", default=None)
    client = models.ManyToManyField(Client, verbose_name="Клиенты")
    send_time = models.DateTimeField(default=timezone.now, verbose_name="Время отправки")
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
        ('stopped', 'Остановлена')
    ]
    status = models.CharField(max_length=10, choices=status_choices, verbose_name="Статус")

    def __str__(self):
        return f"Рассылка № {self.pk}"


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", default=None)
    mailing = models.OneToOneField(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="message")
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Содержание письма")


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", related_name="logs")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время последней попытки")
    status = models.CharField(max_length=10, verbose_name="Статус попытки")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
