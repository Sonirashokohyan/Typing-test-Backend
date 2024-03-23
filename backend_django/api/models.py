from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    REQUIRED_FIELDS =[]
    
class TypingTest(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    wpm = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Typing Test: {self.date} - User: {self.user}'