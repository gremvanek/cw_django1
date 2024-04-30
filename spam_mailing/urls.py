from django.urls import path

from spam_mailing.views import home_page, client_detail, client_create, client_update, client_delete, client_list, \
    MailingCreateView, MailingUpdateView, MailingDeleteView, message_list, MessageCreateView, \
    MessageUpdateView, MessageDeleteView, mailing_list

urlpatterns = [
    path("", home_page, name="home"),

    path("clients/", client_list, name="client_list"),
    path('client/<int:pk>/', client_detail, name='client_detail'),
    path('client/new/', client_create, name='client_create'),
    path('client/<int:pk>/edit/', client_update, name='client_update'),
    path('client/<int:pk>/delete/', client_delete, name='client_delete'),

    path('mailing/', mailing_list, name='mailing_list'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('message/', message_list, name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]
