from django.urls import path

from blog.apps import BlogConfig
from blog.views import blog, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', blog, name='list'),
    path('blog/view/<slug:slug>/', BlogDetailView.as_view(), name='view'),
    path('blog/create/', BlogCreateView.as_view(), name='create'),
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
]
