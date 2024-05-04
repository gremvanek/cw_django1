from django.urls import path

from blog.apps import BlogConfig
from blog.views import blog, BlogDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', blog, name='list'),
    path('blog/view/<slug:slug>/', BlogDetailView.as_view(), name='view'),
]
