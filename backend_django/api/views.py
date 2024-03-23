from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
import jwt, datetime
from .models import TypingTest
from .serializers import TypingTestSerializer
from django.conf import settings


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle token expired error
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token error
        return None

class RegisterView(APIView):
    def post(self, request):
        request_data = request.data.copy()
        password = request_data.pop('password', None)
        
        if password:
            hashed_password = make_password(password)
            request_data['password'] = hashed_password 

        serializer = UserSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success':2})
    
class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        user = authenticate(username = username, password = password)
        if not user:
            return Response(False)
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        response = Response()
        response.data = {'token':token,'name':user.name}
        return response

class LogoutView(APIView):
    def post(self, request):
        c_token = request.data['token']
        payload = verify_jwt_token(c_token)
        user_id = payload.get('user_id')
        
        if(user_id == request.user.id):
            response = Response()
            response.data = True
            return response
        else:
            return Response(False)

class UserView(APIView):
    def post(self, request):
        c_token = request.data['token']
        payload = verify_jwt_token(c_token)
        user_id = payload.get('id')
        user = User.objects.filter(id=user_id).first()
        if(user):
        # print(user.name)
            return Response(user.name)
        else:
            return Response(False)



class RecordView(APIView):
    def post(self, request):
        
        c_token = request.data['token']
        payload = verify_jwt_token(c_token)
        user_id = payload.get('id')
        user = User.objects.filter(id=user_id).first()
        typingTests = TypingTest.objects.filter(user_id = user.id).order_by('-date')[:7]
        serializer = TypingTestSerializer(typingTests,many=True)
        
        if(user):
            return Response(serializer.data)
        else:
            return Response(False)
    
class RecordSave(APIView):
    def post(self, request):
        newWpm = request.data['WPM']
        c_token = request.data['token']
        print(newWpm,c_token)
        payload = verify_jwt_token(c_token)
        user_id = payload.get('id')
        user = User.objects.filter(id=user_id).first()
        saveWpm = TypingTest(user_id = user.id,wpm = newWpm)
        saveWpm.save()
        
        if(user):
            return Response(True)
        else:
            return Response(False)
        


