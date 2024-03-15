from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    REQUIRED_FIELDS =[]
    
class TypingTest(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wpm = models.IntegerField()

    def __str__(self):
        return f'Typing Test: {self.date} - User: {self.user}'