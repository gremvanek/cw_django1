from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from spam_mailing.forms import ClientForm, MailingForm, MessageForm
from spam_mailing.models import Client, Mailing, Message


@login_required
def client_list(request):
    """Отображение списка клиентов."""
    clients = Client.objects.all()
    return render(request, 'spam_mail/client_list.html', {'clients': clients})


@login_required
def client_detail(request, pk):
    """Отображение деталей клиента."""
    client = Client.objects.get(pk=pk)
    return render(request, 'spam_mail/client_detail.html', {'client': client})


@login_required
def client_create(request):
    """Создание нового клиента."""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user  # Присваиваем текущего пользователя владельцем клиента
            client.save()
            return redirect('spam:client_list')
    else:
        form = ClientForm()
    return render(request, 'spam_mail/client_form.html', {'form': form})


@login_required
def client_update(request, pk):
    """Обновление информации о клиенте."""
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('spam:client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'spam_mail/client_form.html', {'form': form})


@login_required
def client_delete(request, pk):
    """Удаление клиента."""
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('spam:client_list')
    return render(request, 'spam_mail/client_delete.html', {'client': client})


class ClientMakeActiveView(View):
    @staticmethod
    def post(request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.make_active()
        return redirect('spam:client_list')


class ClientInactiveView(View):
    @staticmethod
    def post(request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.inactive()
        return redirect('spam:client_list')


@login_required
def mailing_list(request):
    """Отображение списка рассылок."""
    mailings = Mailing.objects.all()
    is_manager = request.user.groups.filter(name='Менеджеры').exists()

    context = {
        'mailings': mailings,
        'is_manager': is_manager,
    }
    return render(request, 'spam_mail/mailing/mailing_list.html', context)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Подробная информация о рассылке."""
    model = Mailing
    template_name = 'spam_mail/mailing/mailing_detail.html'


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание новой рассылки."""
    model = Mailing
    form_class = MailingForm
    template_name = 'spam_mail/mailing/mailing_form.html'
    success_url = reverse_lazy('spam:mailing_list')

    def form_valid(self, form):
        # Получаем данные из формы
        clients = form.cleaned_data['clients']

        # Создаем объект Message
        message = Message.objects.create(subject="Тема письма", body="Содержание письма", owner=self.request.user)

        # Создаем объект Mailing
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.message = message
        mailing.save()

        # Присваиваем клиентов к рассылке
        mailing.clients.set(clients)

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление информации о рассылке."""
    model = Mailing
    form_class = MailingForm
    template_name = 'spam_mail/mailing/mailing_form.html'
    success_url = reverse_lazy('spam:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки."""
    model = Mailing
    success_url = reverse_lazy('spam:mailing_list')


class MailingStopView(View):

    @staticmethod
    def post(request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.stop_mailing()
        return redirect('spam:mailing_list')


@login_required
def message_list(request):
    """Отображение списка сообщений."""
    messages = Message.objects.all()
    return render(request, 'spam_mail/message/message_list.html', {'messages': messages})


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание нового сообщения."""
    model = Message
    form_class = MessageForm
    template_name = 'spam_mail/message/message_form.html'
    success_url = reverse_lazy('spam:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление информации о сообщении."""
    model = Message
    form_class = MessageForm
    template_name = 'spam_mail/message/message_form.html'
    success_url = reverse_lazy('spam:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения."""
    model = Message
    success_url = reverse_lazy('spam:message_list')
