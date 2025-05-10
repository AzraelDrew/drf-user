from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User
from rest_framework import status

class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser','test@app.com','testpassword')

        self.url = reverse('account-create')

    def test_create_user(self):
        """
          确保我们能够创建一个新用户
        """
        
        data = {
            'username':'foobar',
            'email':'foobar@app.com',
            'password':'somepassword'
        }

        response = self.client.post(self.url,data)
        print(response.data)

        # 确保此时数据库中有两个用户
        self.assertEqual(User.objects.count(),2)
        # 请求通过并返回状态码201
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        # 成功创建后可以返回用户名和电子邮箱
        self.assertEqual(response.data['username'],data['username'])
        self.assertEqual(response.data['email'],data['email'])
        self.assertFalse('password' in response.data)

    """
      字段触发错误示例：
          1、未提供密码
          2、密码过短
    """

    def test_create_user_with_short_password(self):
        """
          确保在用户输入的密码少于8位时不能创建用户
        """

        data = {
            'username':'foobar',
            'email':'foobar@app.com',
            'password':'foo'
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(len(response.data['password']),1)
    
    def test_create_user_with_no_password(self):
        """
          确保在用户未提供密码时不能创建用户
        """

        data = {
            'username':'foobar',
            'email':'foobar@app.com',
            'password':''
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(len(response.data['password']),1)

    """
      字段触发错误示例：
          1、用户名已存在
          2、未提供用户名
          3、用户名太长
    """
    def test_create_user_with_preexisting_username(self):
        data = {
          'username':'testuser',
          'email':'foobar@app.com',
          'password':'foobaroo'
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(len(response.data['username']),1)

    def test_create_user_with_no_username(self):
        data = {
          'username':'',
          'email':'foobar@app.com',
          'password':'foobaroo'
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(len(response.data['username']),1)

    def test_create_user_with_too_long_username(self):
        data = {
          'username':'foo'*20,
          'email':'foobar@app.com',
          'password':'foobaroo'
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(len(response.data['username']),1)

    """
      字段触发错误示例：
          1、邮箱已经使用过
          2、未提供邮箱
          3、错误的邮箱格式
    """

    def test_create_user_with_preexisting_email(self):
        data = {
          'username':'admin',
          'email':'test@app.com',
          'password':'foobaroo'
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(len(response.data['email']),1)

    def test_create_user_with_no_email(self):
        data = {
          'username':'admin',
          'email':'',
          'password':'foobaroo'
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(len(response.data['email']),1)

    def test_create_user_with_invalid_username(self):
        data = {
          'username':'foobarbaz',
          'email':'foobar',
          'password':'foobaroo'
        }

        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(len(response.data['email']),1)


class LoginTest(APITestCase):
    
    
    def setUp(self) :
        self.test_user = User.objects.create_user('testuser','test@app.com','testpassword')

        self.url = reverse('user-login')

    
    def test_login_username(self):
        """
          通过用户名登录
        """
        data = {
          'choice':"username",
          'username':'testuser',
          'password':"testpassword"
        }

        response = self.client.post(self.url,data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_login_email(self):
        """
          通过邮箱登录
        """
        data = {
          'choice':"email",
          'email':'test@app.com',
          'password':"testpassword"
        }

        response = self.client.post(self.url,data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
