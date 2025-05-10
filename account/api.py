from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password,check_password
from .serializers import UserSerializer,UserCreateSerializer
from .tokens import create_jwt_pair_for_user
from django.db.models import Q
from .models import User

class UserCreateView(APIView):

    """
      创建用户
    """
    permission_classes = [AllowAny]
    def post(self,request):
        # json -> dict

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def login_use_username(username=None,password=None):

    if username and password:
        origin_password = User.objects.get(username=username).password
        user_password = check_password(password,origin_password)
        if user_password:
            user = User.objects.get(username=username)
            return user
        else:
           return None
    else:
        return None

def login_use_email(email=None,password=None):
    
    if email and password:
        user = authenticate(email=email,password=password)
        return user
    else:
        return None
class LoginView(APIView):
    """
      登录
    """
    permission_classes = [AllowAny]

    def post(self,request):
        choice = request.data.get("choice")
        email = request.data.get("email","")
        username = request.data.get("username","")
        password = request.data.get("password")

        options = {
          "email":login_use_email(email,password),
          "username":login_use_username(username,password)
        }
        user = options[choice]

        if user is not None:
            tokens = create_jwt_pair_for_user(user)

            response = {"message":"登录成功！","tokens":tokens }
            return Response(data=response,status=status.HTTP_200_OK)
        
        else:
            response = {"message":"用户名或密码错误，请重新输入！"}
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)
