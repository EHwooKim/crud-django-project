from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model # 이것도 필요하다!

class CustomUserChangeForm(UserChangeForm):
    class Meta: # 다른건 UserChageForm에서 상속받고 Meta의 fields만 바꾸고 싶은거니까
        model = get_user_model() # get_user_model() : User를 return한다.
        fields = ('username', 'first_name', 'last_name')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')