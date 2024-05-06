from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from blog.models import Blog


# Create your views here.

def blog(request):
    context = {
        'object_list': Blog.objects.all(),
        'title': " Блог",
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

