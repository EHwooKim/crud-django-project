from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.

# 기본 모델을 받아서 나만의 아티클을 생성한다는 느낌

# 1. 모델(스키마) 정의
# 데이터베이스 테이블을 정의하고, 
# 각각의 컬럼(혹은 필드)를 정의

class HashTag(models.Model):
    # 게시글과 다르게 hashtag는 중복을 없애야겠지. 동일한 문자는 같은 pk로 관리가 되게.
    content = models.TextField(unique=True)
    def __str__(self):
        return self.content

    
class Article(models.Model):    # models.Model 을 상속 받는 형식으로 쓴다. ~.~.get()으로 앞으로 데이터 사용하는게 여기 들어있거든
    # id : integer 자동으로 정의(Primary Key)
    # id = models.AutoField(primary_key=True) -> Integer 값이 자동으로 하나씩 증가 (AUTOINCREMENT)
    # CharField -  필수인자로 max_length 지정
    title = models.CharField(max_length=10)  # 기사의 제목을 변수값으로 가지는데 그것은 캐릭터 필드이다. (일종의 스키마를 정의하는거야)
    content = models.TextField()
    image = models.ImageField(blank=True)
    # ImageSpecField : input 하나만 받고 잘라서 저장
    # ProcessedImageField : input 받을 것을 잘라서 저장
    # resize to fill : 300x300으로 자르기
    # resize to fit : 긴쪽(너비 혹은 높이)을 300에 맞추고 비율에 맞게 사용
    image_thumbnail = ImageSpecField(
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality':80},
    )

    # DateTimeField
    #   auto_now_add : 생성시 자동으로 저장
    #   auto_now : 수정시마다 자동으로 저장
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      # 이런식으로 다양한 필드 생성 가능. 다 쓰고나서 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
                                                          # python manage.py makemigrations 해서 마이그레이션 파일 생성 (소원쪽지 같은거라고 보면 된다.) 이러면 migrations 파일이 만들어질거고
                                                          # python manage.py migrate 그 소원쪽지를 적용시켜줘! - db에 반영!
    # 좋아요 기능을 위해 user랑 또 연결을 시킬건데 user는 이미 위에 있으니까
    like_users = models.ManyToManyField(
                                settings.AUTH_USER_MODEL,      # User class랑 연결 시킬건데 models.py에서는 settings.AUTH_USER_MODEL로 한다!
                                related_name = 'like_articles',# through 옵션은 여기서는 필요 없고. user입장에서 user.articles_set.all()을 했을때
                                blank=True                     # 작성글, 좋아요글 구분을 위해 related_name은 필요하다
                                )                              # blank_True: 좋아요 처음부터 있는거 아니니까
    hashtags = models.ManyToManyField(
                                HashTag,
                                related_name='articles',        # 이 줄 안쓰면 hashtag.article_set 이렇게 접근하면 되겠지
                                blank=True
                                )


    def __str__(self):
        return f'<{self.id}> : {self.title}'


class Comment(models.Model):
    content = models.CharField(max_length=140)
    created_at = models.DateField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # on_delete
    # 1. CASCADE : 글이 삭제되었을 때 모든 댓글을 삭제
    # 2. PROTECT : 댓글이 존재하면 글 삭제 안됨.
    # 3. SET_NULL : 글이 삭제되면 NULL로 치환(NOT NULL일 경우 옵션 사용X)
    # 4. SET_DEFAULY : 디폴트 값으로 치환.


# models.py에서 - python 클래스 정의
#               - 모델 설계도
# makemigrations - migration 파일 생성
#                - DB 설계도 작성 !
# migrate - 위의 설계도, migration 파일 DB 반영

# #--------------------------------------------------------
# # 상속관련 추가내용 이렇게 상속받아서 원하는대로 만들수가 있다
# class TimeStampMixin(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)  
#     updated_at = models.DateTimeField(auto_now=True)
# # 이렇게 해놓고 
# class Artivle(TimeStampMixin):
#     pass
# # 같이 상속받으면 생성, 수정시간이 기본적으로 들어가게 되겠지!