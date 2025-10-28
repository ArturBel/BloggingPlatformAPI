from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=64)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # preventing double hashing
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Tech', 'Technology'),
        ('Personal', 'Personal matters'),
        ('Wellness', 'Health and Wellbeing'),
        ('Trivia', 'Trivia')
    ]

    title = models.CharField(unique=False, max_length=64)
    content = models.CharField()
    category = models.CharField(choices=CATEGORY_CHOICES, default='Trivia')
    tags = ArrayField(models.CharField(max_length=32), blank=True, default=list)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Posts')
