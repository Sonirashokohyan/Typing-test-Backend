from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from .models import TypingTest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'password']
        

class TypingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypingTest
        fields = ['wpm']