from django.contrib import admin

from .models import Client, Mailing, Message, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name', 'middle_name', 'comment', 'owner')
    search_fields = ('email', 'last_name', 'first_name', 'middle_name', 'comment')
    list_filter = ('owner',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('date_start', 'period', 'status', 'owner')
    search_fields = ('date_start', 'period', 'status')
    list_filter = ('owner',)
    readonly_fields = ('owner',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'subject', 'body', 'owner')
    search_fields = ('mailing', 'subject', 'body')
    list_filter = ('owner',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'last_time_mail', 'status', 'response')
    search_fields = ('mailing', 'last_time_mail', 'status', 'response')
