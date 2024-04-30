from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from spam_mailing.forms import ClientForm, MailingForm, MessageForm
from spam_mailing.models import Client, Mailing, Message


def home_page(request):
    return render(request, 'index.html')


def client_list(request):
    clients = Client.objects.all()
    return render(request, 'spam_mail/client_list.html', {'clients': clients})


def client_detail(request, pk):
    client = Client.objects.get(pk=pk)
    return render(request, 'spam_mail/client_detail.html', {'client': client})


def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('spam:client_list')
    else:
        form = ClientForm()
    return render(request, 'spam_mail/client_form.html', {'form': form})


def client_update(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('spam:client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'spam_mail/client_form.html', {'form': form})


def client_delete(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('spam:client_list')
    return render(request, 'spam_mail/client_delete.html', {'client': client})


def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'spam_mail/mailing/mailing_list.html', {'mailings': mailings})


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'spam_mail/mailing/mailing_form.html'
    success_url = reverse_lazy('spam:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'spam_mail/mailing/mailing_form.html'
    success_url = reverse_lazy('spam:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('spam:mailing_list')


def message_list(request):
    messages = Message.objects.all()
    return render(request, 'spam_mail/message/message_list.html', {'messages': messages})


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'spam_mail/message/message_form.html'
    success_url = reverse_lazy('spam:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'spam_mail/message/message_form.html'
    success_url = reverse_lazy('spam:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('spam:message_list')
