from django.contrib.auth.mixins import UserPassesTestMixin  # Импортируем миксин для проверки пользователя
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


# Create your views here.

def blog(request):
    context = {
        'object_list': Blog.objects.all(),
        'title': "Блог",
    }
    return render(request, 'blog/blog_list.html', context)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Blog, id=slug)
        # Увеличиваем счетчик просмотров здесь
        obj.views_count += 1
        obj.save()
        self.object = obj  # Устанавливаем self.object
        return obj


class BlogCreateView(UserPassesTestMixin, CreateView):  # Добавляем UserPassesTestMixin
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')

    def test_func(self):  # Определяем функцию для проверки прав пользователя
        return self.request.user.is_superuser  # Возвращаем True, если пользователь является суперпользователем


class BlogUpdateView(UserPassesTestMixin, UpdateView):  # Добавляем UserPassesTestMixin
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')

    def test_func(self):  # Определяем функцию для проверки прав пользователя
        return self.request.user.is_superuser  # Возвращаем True, если пользователь является суперпользователем


class BlogDeleteView(UserPassesTestMixin, DeleteView):  # Добавляем UserPassesTestMixin
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')

    def test_func(self):  # Определяем функцию для проверки прав пользователя
        return self.request.user.is_superuser  # Возвращаем True, если пользователь является суперпользователем
