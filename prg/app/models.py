from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    birth_date = models.DateField()
    role = models.CharField(max_length=20, choices=[
        ('customer', 'Заказчик'),
        ('executor', 'Исполнитель'),
    ])

    def __str__(self):
        return f"{self.user.username}'s Profile"