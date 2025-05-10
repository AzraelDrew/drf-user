# 使用django-extensions运行脚本
# runscript 命令
from pprint import pprint
from django.db.models import Q

from account.models import User


def run():
    login_select = User.objects.filter(Q(username='admin') | Q(email='admin@ad.com'))
    pprint(login_select)