# 소셜로그인 (`OAuth - Open Authentication` 인증체계)

* `OAtu 2.0` 버전

* `auth` 두가지 의미
  * authentication (인증- 로그인)
  * authorization (권한 - 로그인 이후)
  * 이 두가지를 다 포함 하는 `django allauth` [공식문서](https://django-allauth.readthedocs.io/en/latest/installation.html)
    * 장고는 kakao 지원해서 좋아
* `$ pip install django-allauth`

* 이것저것추가...카카오페개발자 설정...

```txt
REST API키 (열쇠) <= admin 페이지에서 클라이언트 아이디
38a9bb0a93a13c554b0782dcf13fba00


Client Secret (비밀번호) <= admin 페이지에서 비밀 키
MPP470u5L1Oir6cDjBdxqO8BofTQgAR9
```

* 장고는 기본적으로 `admin` 지원하기 때문에 API키 관리가 쉽다.
  * admin페이지 -> 소셜 어플리케이션
  * 제공자, 이름, 클라이언트 아이디, 비밀 키 추가. Sites: example.com 더블클릭 (SITE_ID=1해놔서 기본설정 되어있는거)

* 이제 기본설정 끝. 로그인창에 카카오 추가하자 [공식문서]( https://django-allauth.readthedocs.io/en/latest/templates.html#social-account-tags )

  ```html
  <!-- login.html -->
  <a href="{% provider_login_url 'kakao' %}">
  카카오 로그인
  </a>
  ```

  

* 카카오 로그인 과정

  ```text
  1. 사용자가 카카오링크(/accounts/kakao/login)
  2. 사용자는 카카오 사이트 로그인 페이지를 확인
  3. 사용자는 로그인 정보를 카카오로 보냄
  4. 카카오는 redirect url로 django 서버로 사용자 토큰을 보냄
  5. 해당 토큰을 이용하여 카카오에 인증 요청
  6. 카카오에서 확인
  7. 로그인
  ----------------------------------
  토근(access token)은 보통 유효기간이 있는데,
  refresh token을 통해서 토근 재발급을 받을 수 있다.
  ```

  ```text
  * 각각을 다음과 같이 부른다아
  카카오 - 리소스 서버/인증 서버
  사용자(리소스 owner) - 유저
  django - 클라이언트
  ```
