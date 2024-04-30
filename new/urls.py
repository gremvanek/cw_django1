from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(('spam_mailing.urls', 'spam_mailing'), namespace='spam')),
    path('', include(('user.urls', 'user'), namespace='user')),
]
