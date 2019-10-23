from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import login as auth_login # login이라는 함수 우리가 정의해서 쓰고있어서 헷갈리지않게 이름 변경
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash # 이게 비번 바꾸고 로그인해주는거
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from IPython import embed

from .forms import CustomUserChangeForm, CustomUserCreationForm


# Create your views here.

# articles할 때는 모델 정의 -> 모델폼 -> create 로직 이었는데
# accounts 관련 로직이 있어서 그걸 활용할거고 UserCreationForm이야
def signup(request):
    # 로그인되어있는 사람이 회원가입하려할때 돌려보내기
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 회원가입 후 바로 로그인되는 사이트의 방법
            # user = form.save()
            # auth_login(request, user)            
            # 바로 로그인 안되는 사이트
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)


# 로그인은 인증과 관련된 폼, Authentication
def login(request):
    # 로그인되어 있는 사람이 로그인 시도할 때 되돌려 보내기
    if request.user.is_authenticated:
        return redirect('articles:index')    
    if request.method == 'POST':
        # authen-form 은 모델폼이 아니라 인자 순서가 다음과 같이 다르고, request는 그럼 왜 넣느냐. request에 정보가 다 담겨있기 때문이지.
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 로그인 함수 호출
            # AuthenticationForm 은 모델폼 아니고 fomrs.form이라  .get_user(), return 값이 User instance야
            user = form.get_user()
            auth_login(request, user)
            # 또는 위의 두 줄을 합쳐서
            # auth_login(request, form.get_user()) 처럼 써도 오키
            # next를 달오고면 앞에꺼, next 안달고.. login 버튼 눌러서 오는거면 뒤에꺼.. 단축평가!
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def update(request):
    # if not request.user.is_authenticated:
    #     return redirect('articles:index') 이거보다 login_required가 더 좋네
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user) 
    context = {
        'form':form
    }
    return render(request, 'accounts/form.html', context)


@login_required
def password_change(request):
    # model form이 아니라 그냥 form이라서 반드시 첫번쨰 인자로 user를 넘겨줘야 한다.
    if request.method == 'POST':
        # 인자로 user정보 먼저 넘겨줘야 한다는 것이 포인트!
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            # 비밀번호 바뀌는 순간 그 전에 저장되어있던 세션의 정보(비밀번호)가 달라져서 로그아웃된다.
            form.save()
            update_session_auth_hash(request, form.user) # request랑 user정보인데 user 정보는 form 에서
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form
    }
    return render(request, 'accounts/form.html', context)


def profile(request, account_pk):
    # user = User.objects.get(pk=account_pk) 이거 아니다아
    User = get_user_model()  # user model은 이렇게 불러온다고 생각하랬지
    user = get_object_or_404(User, pk=account_pk) # 여기에서 특정 유저를 불러오는 거고
    context = {
        'user_profile': user
    }
    return render(request, 'accounts/profile.html', context)


def follow(request, account_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=account_pk) # 이 user가 obama
    if user != request.user:
        # user(obama)를 팔로우한적 있다면
        if request.user in user.followers.all():
        # if user in request.user.followings.all(): 위랑 이거랑 같은거겠지
            # 취소
            user.followers.remove(request.user)
        # 아니면
        else:
            # 팔로우
            user.followers.add(request.user)
    return redirect('accounts:profile', user.pk)


