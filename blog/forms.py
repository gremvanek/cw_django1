from django import forms

from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body', 'preview', 'date_is_published', 'views_count']
