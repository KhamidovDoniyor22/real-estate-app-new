from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_agent = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
