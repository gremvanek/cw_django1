from django.contrib import admin
from django.urls import path

from spam_mailing.views import home_page, client_detail, client_create, client_update, client_delete, client_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_page, name="home"),
    path("clients/", client_list, name="client_list"),
    path('client/<int:pk>/', client_detail, name='client_detail'),
    path('client/new/', client_create, name='client_create'),
    path('client/<int:pk>/edit/', client_update, name='client_update'),
    path('client/<int:pk>/delete/', client_delete, name='client_delete'),
]
