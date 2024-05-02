from django.urls import path

from spam_mailing.views import client_detail, client_create, client_update, client_delete, client_list, \
    MailingCreateView, MailingUpdateView, MailingDeleteView, message_list, MessageCreateView, \
    MessageUpdateView, MessageDeleteView, mailing_list, MailingDetailView, MailingStopView, ClientMakeActiveView, \
    ClientInactiveView

urlpatterns = [

    path("clients/", client_list, name="client_list"),
    path('client/<int:pk>/', client_detail, name='client_detail'),
    path('client/new/', client_create, name='client_create'),
    path('client/<int:pk>/edit/', client_update, name='client_update'),
    path('client/<int:pk>/delete/', client_delete, name='client_delete'),
    path('client/<int:pk>/make_active/', ClientMakeActiveView.as_view(), name='client_make_active'),
    path('client/<int:pk>/inactive/', ClientInactiveView.as_view(), name='client_inactive'),

    path('mailing/', mailing_list, name='mailing_list'),
    path('mailing/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/<int:pk>/stop/', MailingStopView.as_view(), name='mailing_stop'),

    path('message/', message_list, name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]
