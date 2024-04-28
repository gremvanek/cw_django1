from django.db import models


class Client(models.Model):
    objects = models.Manager()
    email = models.EmailField(verbose_name="Email")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}, {self.middle_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def make_active(self):
        self.is_active = True
        self.save()

    def inactive(self):
        self.is_active = False
        self.save()

