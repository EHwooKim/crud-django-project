[pythonUser](https://github.com/django/django/blob/master/django/contrib/auth/models.py)



user 생성시 `UserCreationForm` 썼었지

로그인은 `from django.contrib.auth import logout , logout` 썼고

`AuthenticationForm` 또한 활용했는데 이것은 ModelForm이 아니다

로그인이 되어있다는 정보는 `request`에 담겨있다(장고에서는), 실제로는 쿠키와 세션을 통해 활용중이다.



User 클래스는 `models.Model -> AbstarctBaseUser(비밀번호, 로그인시점) -> AbstractUser(username...email 등)` 을 상속받는다

> shell_plus 에서 User.mro()  해보면 위의 상속 순서가 나온다



* [회원정보수정]( https://github.com/django/django/blob/master/django/contrib/auth/forms.py )

  * 회원 생성시에는 `UserCreationForm` 썼지만 수정떄는 왠지 아닐거같지?

  * 수정할 때는 ` UserChangeForm ` 을 쓴다. 

  * `UserChangeForm() `해서 form을 출력하면 원치않은 정보까지 다 나온다... 어떻게 해결할 수 있을까?

  * `상속!!!` 받아서 원하는 것만 가져올 수 있겠지.

  * `accounts` 앱에서 `form.py` 만들고, 

    ```python
    #form.py 에서!
    from django.contrib.auth.forms import UserChangeForm
    
    class CustomUserChangeForm(UserChangeForm): 와 같이 상속받으면 되겠지
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')    
    그리고 추가적으로 필요한 것이 
    from django.contrib.auth import get_user_model !!
    ```

    > 왜 get_user_model()을 쓰는걸까?
    > 그르게...
  
* `views.py`에서 `request.user`를 쓰게 되면 `@login_required` 꼭 생각하기



### 왜 자동으로 login 페이지로 가요?

[참고문서]( https://docs.djangoproject.com/en/2.2/topics/auth/default/#the-login-required-decorator )

>  default값이기 때문이다.!

### 비밀번호 바꾸기

[PasswordChangeForm]( https://github.com/django/django/blob/master/django/contrib/auth/forms.py )

[비밀번호 변경 후 자동 로그인]( https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.update_session_auth_hash )







# User-Article-Comment

* 유저 - 게시글 - 댓글 연결[참고]( https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project )

article model에 정보 추가하려면 그냥 model 에서 한줄 넣으면 되지만

user에 정보 추가하려면 장고 저 밑바닥에 있는 코드르 고칠 수 없으니 상속을 받아서 하면 되겠지만,,, 문제는 앱이 달라..! migrate 하면 table에 앱이름_모델명 이렇게 생기는데 그에 맞게 다 바꿔줘야한다...? 그런 번거로움을 해결해 주는 것이 `AbstractUser 상속`

```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass
```

```python
# settings.py
AUTH_USER_MODEL = 'accounts.User' #default - 'auth.User'
```

[참고]( https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#changing-to-a-custom-user-model-mid-project )

```python
# articles/models.py
from django.conf import settings
user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

```



* [장고  실행과정]( https://docs.djangoproject.com/en/2.2/ref/applications/#how-applications-are-loaded )

  1. INSTALLED_APPS에서 하나씩 import한다

  2. 그러고 models를 import하는 시도를 한다.(model 검증)

     그 과정에서 user = models.ForeignKey(User...) 같이 적으면  아직 User 클래스가 정의되지 않은 모델에서 오류가 날 수도 있어서

     `user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)`와 같이 쓰는 것이다.





User모델을 숨겨놓은거 쓸 수 도있는데 꺼내놓고 쓰라고  장고 문서에서 말하는거야

모델폼이나 그런것들은 기존에 만들어진 것을 쓰는것이다(모델폼상속)

uset = 'AUTH_USER_MODEL' ('~~'값에 따라 바뀐다는 뜻.)

위처럼 변수화를 해서 바꾸는게 아닌 다른 방법으로 하면 장고 내부의 user를 쓰는 다양한 코드에서 user를 제대로 활용을 못하거든.

get_user_model은 AUTH~MODEL에  설정된 user를 불러다주는 기능이다.

user model을 불러올 때 `from accounts.models import User` 같이 불러오는게 아니라 

`from django.contrib.auth import get_user_model`이라는 함수를 불러와서 쓰는거지.



1. User는 pass로 비워두더라고 빼놓고 써라! 확장 가능성을 위해.

2. 그 뺴놓은 위치를 settings.py에서 정의를 해주는거지.

3. 그러고 get_user_model로 불러오자

4. models.py에서 user class를 불러올 때 클래스로 잘못 불러오면 정의되기 전에 불러올 수도 있어서 오류가 날 수 있으니 `settings.AUTH_USER_MODEL`로 불러오자

   >  `settings.AUTH_USER_MODEL` :`accounts.User (str)`

5.  정리: User클래스를 내가 가져다 쓰고싶다.(views.py 나 models.py같이)면! `get_user_model`에서 쓰고 models.py에서는 `settings.AUTH_USER_MODEL`로 쓰자

   



이렇게 까지만하면 회원가입도 안되는데 UserCreationForm에 model=User로 되어있어서 그렇거든..

답은! 상속이다. Custom으로 내가 만든 user를 가져온다! (by. get_user_model())



### User 탁쌤의 정리

* 장고는 User 관련 기능이 내부적으로 있다 -> 가져다가 쓰면 됨.

* django.contrib.auth.models.User 변경할 상황이 분명히 생긴다!

  -> 상속받아서 내가 User를 새로 만들면 됨.

  -> 그런데! 나중에 상속받아서 만들기에는 DB에 연결이 되어있어서

  -> 다~~바꾸기 어렵다!

  -> 그러니 프로젝트를 만들면서 미리 해라!! 라고 장고가 추천한다

  -> 그런데 그 바꾼 User를 장고가 '내부'에서 어떻게 알지?

  -> settings 설정의 AUTH_USER_MODEL 을 설정해준다아!!

  -> 그러면 이제 User 클래스를 어떻게 가져다 쓰는데?

  -> get_user_model()로 가져다 쓴다!! (settings  설정을 본다.)

* 그러면!! models.py에서도 get_user_model()쓸 수 있음??????

  -> 아닐 수 있다!!!!!!

  -> 왜냐하면! 장고가 명령어를 수행 할 때, INSTALLED_APPS -> models / apps 의 순서로 확인을 하는데!!!

  -> 그 과정에서 User클래스가 아직 없을 수 있다 ( 이름이 생성안되었거나 import가 아직 안댔거나)

  -> 그떈 그냥 settings.AUTH_USER_MODEL로 `문자열`을 찍어 놓으면!! 알아서 바꿔준다!!!!

* 프로젝트를 시작과 동시에 User 모델을 뺴놓자! (pass로 일단 비워두더라고)

  -> User 클래스가 필요하면, get_user_model()호출해서 쓰자. 

  -> models.py에서만 settings.AUTH_USER_MODEL 쓰고!!!

* 그런데 바꾸고 보니 갑자기 UserCreationForm을 못쓰네!!????왜지!!!

  -> 실제로 UserCreationForm 내부 코드를 보면 바보같이 [User를 그대로 import해서 써서 그렇다]( https://github.com/django/django/blob/master/django/contrib/auth/forms.py ) - 		링크 94번째 줄

  (from django.contrib.auth.models import User  )

  -> 혼나야함. get_user_model()로 써야 맞는건데에!!

  -> 그럼 어떻게 바꾼다????? UserCreationForm 자체를 바꾸는건 못하니까아!!!

  -> `상속`받아서 내가 원하는대로 바꾸면 되겠지!!!

  ```python
  class CustomUserCreationForm(UserCreationForm):
      class Meta:
          model = get_user_model()  # 이부분이 User였던건데 상속으로 내가 바꾼거지
          fields = ('username', 'first_name', 'last_name')
  ```
















user = models.ForeignKey(User, on_delete=models.CASCADE)



from django.contrib.auth import get_user_model