from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Django에서는 프로젝트를 시작할 때 다음과같이 User Class를 직접 만드는 것을 추천한다! (pass로 일단 비워두더라도)
class User(AbstractUser):
    pass


