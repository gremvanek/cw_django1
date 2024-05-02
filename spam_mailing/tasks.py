# tasks.py
import smtplib
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
from django.utils import timezone

from .models import Mailing, MailingLog

schedulers = {}


def send_emails(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)

    if mailing.status == 'stopped':
        # Если статус рассылки "Остановлена", выходим из функции
        return

    # Проверяем, отправлялось ли сообщение уже сегодня для рассылки с частотой 'daily'
    if mailing.frequency == 'daily':
        today = timezone.now().date()
        last_successful_attempt = mailing.logs.filter(timestamp__date=today, status='success').last()
        if last_successful_attempt:
            # Сообщение уже было успешно отправлено сегодня, выводим сообщение и завершаем функцию
            print("Сообщение уже было успешно отправлено сегодня")
            mailing.status = 'completed'
            mailing.save()
            return

    # Проверяем, отправлялось ли сообщение уже в этой неделе для рассылки с частотой 'weekly'
    if mailing.frequency == 'weekly':
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Начало недели
        end_of_week = start_of_week + timedelta(days=6)  # Конец недели
        last_successful_attempt = mailing.logs.filter(timestamp__date__range=[start_of_week, end_of_week],
                                                      status='success').last()
        if last_successful_attempt:
            # Сообщение уже было успешно отправлено на этой неделе, выводим сообщение и завершаем функцию
            print("Сообщение уже было успешно отправлено на этой неделе")
            mailing.status = 'completed'
            mailing.save()
            return

    # Проверяем, отправлялось ли сообщение уже в этом месяце для рассылки с частотой 'monthly'
    if mailing.frequency == 'monthly':
        today = timezone.now().date()
        start_of_month = today.replace(day=1)  # Начало месяца
        end_of_month = start_of_month.replace(day=1, months=1) - timedelta(days=1)  # Конец месяца
        last_successful_attempt = mailing.logs.filter(timestamp__date__range=[start_of_month, end_of_month],
                                                      status='success').last()
        if last_successful_attempt:
            # Сообщение уже было успешно отправлено в этом месяце, выводим сообщение и завершаем функцию
            print("Сообщение уже было успешно отправлено в этом месяце")
            mailing.status = 'completed'
            mailing.save()
            return

    # Подключаемся к SMTP-серверу
    server = smtplib.SMTP_SSL(config('EMAIL_HOST'), config('EMAIL_PORT', cast=int))
    server.login(config('EMAIL_HOST_USER'), config('EMAIL_HOST_PASSWORD'))

    # Get the message associated with the mailing
    message = mailing.message

    for client in mailing.client.filter(is_active=True):
        email_message = MIMEMultipart()
        email_message['From'] = config('EMAIL_HOST_USER')
        email_message['To'] = client.email
        email_message['Subject'] = message.subject
        email_message.attach(MIMEText(message.body, 'plain'))

        try:
            server.sendmail(config('EMAIL_HOST_USER'), client.email, email_message.as_string())
            status = 'success'
            server_response = 'Email sent successfully'
        except smtplib.SMTPException as e:
            status = 'failed'
            server_response = str(e)

        MailingLog.objects.create(
            mailing=mailing,
            timestamp=timezone.now(),
            status=status,
            server_response=server_response
        )

    # Update the mailing status to 'completed'
    mailing.status = 'completed'
    mailing.save()

    # Отключаемся от SMTP-сервера
    server.quit()

    # Remove the scheduler from the global dictionary
    if mailing_id in schedulers:
        del schedulers[mailing_id]


def start_scheduler(mailing_id):
    # Check if a scheduler is already running for this mailing_id
    if mailing_id in schedulers:
        print(f"Задача уже запущенна для рассылки {mailing_id}")
        return

    mailing = Mailing.objects.get(id=mailing_id)
    mailing.send_time = timezone.now()
    mailing.save()

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_emails, args=[mailing_id])
    scheduler.start()

    # Add the scheduler to the global dictionary
    schedulers[mailing_id] = scheduler
