# Django Authentication 

## 1. `User` Class

* [기본 문서](https://docs.djangoproject.com/en/2.2/topics/auth/default/#user-objects)

> django에서는 프로젝트를 시작할 때, 항상 `User` Class를 직접 만드는 것을 추천함! [링크 - custom user model](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model)
>
> django의 기본 Authentication과 관련된 설정 값들을 활용하기 위해 `accounts` 앱으로 시작하는 것을 추천함! (예 - LOGIN_URL = '/accounts/login/')

1. `models.py`

   ```python
   # accounts/models.py
   from django.contrib.auth.models import AbstractUser
   
   class User(AbstactUser):
       pass
   ```

   * django 내부에서 `User` 를 기본적으로 사용한다. 예) `python manage.py createsuperuser` 
   * 확장 가능성(변경)을 위해 내가 원하는 앱에 class를 정의!
   * `User` 상속 관계 [Github 링크](https://github.com/django/django/blob/master/django/contrib/auth/models.py#L384) [공식문서 링크 - auth](https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#fields) 
     *  `AbstactUser` : `username`, `last_name`, `first_name`, `email` , ...
     *  `AbstractBaseUser` : `password` , `last_login` 
     * `models.Model`

2. `settings.py`

   ```python
   # project/settings.py
   
   AUTH_USER_MODEL = 'accounts.User'
   ```

   * `User` 클래스를 활용하는 경우에는 `get_user_model()` 을 함수를 호출하여 사용한다.

     ```python
     # accounts/forms.py
     from django.contrib.auth import get_user_model
     
     class CustomUserCreationForm(UserCreationForm):
         class Meta:
             model = get_user_model()
     ```

   * 단, `models.py`  에서 사용하는 경우에는 `settings.AUTH_USER_MODEL` 을 활용한다. [공식문서 - settings](https://docs.djangoproject.com/en/2.2/ref/settings/#auth-user-model)

     ```python
     # articles/models.py
     from django.conf import settings
     
     class Article(models.Model):
         user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     ```

   *  [공식문서 - Referencing the `User` model](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#referencing-the-user-model)
   
3. `admin.py`

   * admin 페이지를 활용하기 위해서는 직접 작성을 해야 한다.

   * `UserAdmin` 설정을 그대로 활용할 수 있다.

     ```python
     # accounts/admin.py
     from django.contrib.auth.admin import UserAdmin
     from .models import User
     
     admin.site.register(User, UserAdmin)
     ```

     

## 2. Authentication Forms

* [공식문서 - Custom users and the built-in auth forms](https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms)

### 1. `UserCreationForm` : `ModelForm`

* custom user를 사용하는 경우 직접 사용할 수 없음. 
  * 실제 코드 상에 `User`가 직접 import 되어 있기 때문. [Github 링크 - UserCreationForm](https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L94)

```python
# accounts/forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)
```

* `ModelForm` 이므로 활용 방법은 동일하다.

### 2. `UserChangeForm` : `ModelForm`

* custom user를 사용하는 경우 직접 사용할 수 없음.
* 그대로 활용하는 경우 `User`와 관련된 모든 내용을 수정하게 됨.
  * 실제 코드 상에 필드가  `'__all__'` 로 설정되어 있음. [Github 링크 - UserChangeForm](https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L144)

```python
# accounts/forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', ...)
```

### 3. `AuthenticationForm`

* `ModelForm` 이 아님! **인자 순서를 반드시 기억하자!**
* `AuthenticationForm(request, data, ...)` : [Github 링크 - AuthenticationForm](https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L183)

```python
form = AuthenticationForm(request=request, data=request.POST)
if form.is_valid():
    user = form.get_user()
```

* 로그인에 성공한 `user`의 인스턴스는 `get_user()` 메소드를 호출하여 사용한다.

* 실제 로그인은 아래의 함수를 호출하여야 한다. [공식문서 링크](https://docs.djangoproject.com/en/2.2/topics/auth/default/#how-to-log-a-user-in)

  ```python
  from django.contrib.auth import login as auth_login
  auth_login(request, user)
  ```

* 로그인 여부에 따른 접근 제어는 직접 하거나 데코레이터를 활용한다. [공식문서 링크](https://docs.djangoproject.com/en/2.2/topics/auth/default/#limiting-access-to-logged-in-users)

### 4. `PasswordChangeForm`

* `ModelForm` 이 아님! **인자 순서를 반드시 기억하자!**

* `PasswordChangeForm(user, data)`

  ```python
  if request.method == 'POST':
  	form = PasswordChangeForm(request.user, request.data)
  else:
      form = PasswordChangeForm(request.user)
  ```

* 비밀번호가 변경이 완료된 이후에는 기존 세션 인증 내역이 바뀌어서 자동으로 로그아웃이 된다. 아래의 함수를 호출하면, 변경된 비밀번호로 세션 내역을 업데이트 한다. [공식문서 링크](https://docs.djangoproject.com/en/2.2/topics/auth/default/#session-invalidation-on-password-change)

  ```python
  from django.contrib.auth import update_session_auth_hash
  update_session_auth_hash(request, form.user)
  ```



## Appendix. import

```python
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstactUser
from django.contrib.auth.models import AbstactBaseUser
from django.contrib.auth.decorators import login_required
```

```python
from django.conf import settings
```

```python
from django.db import models # models.Model, models.CharField().....
from django import forms # forms.ModelForm, forms.Form
```

```python
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
```














