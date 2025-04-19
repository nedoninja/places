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
    

class Service(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='feedbacks')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.service.title} by {self.author.username}"