from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Django에서는 프로젝트를 시작할 때 다음과같이 User Class를 직접 만드는 것을 추천한다! (pass로 일단 비워두더라도)
class User(AbstractUser):
    followers = models.ManyToManyField(
                    settings.AUTH_USER_MODEL,
                    related_name='followings',
                    blank=True
                    )
