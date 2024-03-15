from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView
from django.urls import path
from .views import RecordView
from .views import RecordSave

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('records/', RecordView.as_view(), name='logout'),
    path('records-save/', RecordSave.as_view(), name='records-save'),
]
