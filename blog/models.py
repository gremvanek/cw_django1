from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blogs/', **NULLABLE, verbose_name='Изображение')
    date_is_published = models.DateField(**NULLABLE, verbose_name='Дата публикации')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блоговая запись'
        verbose_name_plural = 'блоговые записи'
