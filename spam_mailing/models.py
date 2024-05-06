# spam.mailing.py
from django.db import models
from django.utils import timezone

from new import settings
from user.models import User


class Client(models.Model):
    objects = models.Manager()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", default=None)
    email = models.EmailField(verbose_name="Email")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")

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


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", default=None)
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Содержание письма")


class Mailing(models.Model):
    objects = models.Manager()

    PERIOD_CHOICES = [
        ('раз в день', 'раз в день'),
        ('раз в неделю', 'раз в неделю'),
        ('раз в месяц', 'раз в месяц'),
    ]
    STATUS_CHOICES = [
        ('создана', 'создана'),
        ('завершена', 'завершена'),
        ('запущена', 'запущена'),
    ]
    name = models.CharField(max_length=100, verbose_name='Название рассылки', default='Рассылка')
    clients = models.ManyToManyField(Client, verbose_name='Кому (клиенты сервиса)')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение", blank=True, null=True)
    date_start = models.DateField(verbose_name='Дата начала рассылки', default=timezone.now)
    date_next = models.DateTimeField(verbose_name="следующая дата рассылки", default=timezone.now)
    date_end = models.DateField(verbose_name='Дата окончания рассылки', default=timezone.now)
    start_time = models.TimeField(verbose_name='Время рассылки', default=timezone.now)
    period = models.CharField(max_length=30, choices=PERIOD_CHOICES, verbose_name='Периодичность рассылки',
                              default='раз в день')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name='Статус рассылки',
                              default='создана')
    is_active = models.BooleanField(default=True, verbose_name='Активация рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='автор')

    def __str__(self):
        return f'{self.name}: Дата начала: {self.date_start}, Дата окончания: {self.date_end}. Статус: {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ("set_is_active", "Активация рассылки")
        ]

    def stop_mailing(self):
        self.status = 'завершена'
        self.save()


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    last_time_mail = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=50, verbose_name='Статус попытки')
    response = models.TextField(verbose_name='Ответ сервера', null=True, blank=True)

    def __str__(self):
        return (f'Дата и время последней попытки: {self.last_time_mail}.'
                f' Статус попытки:{self.status}')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
