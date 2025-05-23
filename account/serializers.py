from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=20,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8,write_only=True)

    def create(self,validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])

        return user

    class Meta:
        model = User
        fields = ('id','username','email','password')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"