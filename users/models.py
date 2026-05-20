from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_type = models.CharField(
        max_length=10,
        choices=[('customer', 'Покупатель'), ('supplier', 'Поставщик')],
        default='customer',
        verbose_name='Тип пользователя'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')

    def __str__(self):
        return self.username