import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self,username,email,password,**extra_fields):
        if not email:
            raise ValueError("请提供正确的Email")
        if not password:
            raise ValueError("请提供密码")
        user = self.model(
          username=username,
          email=self.normalize_email(email),
          **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self,username,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)

        return self._create_user(username,email,password,**extra_fields)

    def create_superuser(self,username,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self._create_user(username,email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    GENDER_CHOICES = (
        (1,'male'),
        (2,'female'),
        (3,'other')
    )

    # 在AbstractBaseUser中，有密码、最后登录时间，和是否可用(is_active)具备默认值
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True,max_length=254)
    username = models.CharField(max_length=50)

    avatar = models.ImageField(blank=True,null=True)
    desc = models.TextField(blank=True,null=True)
    mobile = models.CharField(max_length=50,blank=True,null=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES,blank=True,null=True)

    is_active = models.BooleanField(default=True)     # 必需字段，否则无法使用新创建用户登录至django-admin
    is_staff = models.BooleanField(default=False)  # 必需字段，否则无法使用新创建用户登录至django-admin
    is_superuser = models.BooleanField(default=False)   # 该字段继承于PermissionsMixin

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'app_user'
