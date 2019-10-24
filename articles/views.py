from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from .forms import ArticleForm, CommentForm
from django.contrib import messages
from IPython import embed
import bootstrap4
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden # 시험에서 이건 안나온다



from .models import Article, Comment, HashTag
# Create your views here.

def index(request):
    # articles = Article.objects.all()[0:10] 
    # print(request.scheme)
    # print(request.method)
    # print(request.get_host())
    # print(request.get_full_path())
    # print(request.build_absolute_uri()) #이렇게 request 오브젝트에는 다양한 정보가 담겨있다
    articles = Article.objects.order_by('-id') # 작성
    # embed()
    context = {
        'articles': articles
    }
    # embed()
    return render(request, 'articles/index.html', context)

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'articles/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
    # (POST) 요청 -> 검증 및 저장
        article_form = ArticleForm(request.POST, request.FILES)
        # 검증 프론트엔드에서 막은걸로 끝이 아니다..!
        if article_form.is_valid():
        # 검증에 성공하면 저장하고
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            # article.save()
            # meta 어쩌구 이후로는 바로 이렇게만 해도 된다
            article = article_form.save(commit=False)
            # user instance를 가져와야한다. 그건 어디에 있다? requset.user
            article.user = request.user
            article.save()
            ## !--- HashTag 저장 및 연결 작업---! [article의 pk가 있어야 M:N관계를 연결해줄수 있을테니 여기서 해야겠지]
            
            for word in article.content.split():
                if word.startswith('#'):
                    # if HashTag.objects.filter(content=word).exists(): # exists()없이도 되는데 있으면 다 가져와서 뭘 하는게 아닌 존재여부만 알려주니 좋지
                    #     HashTag.objects.get(content=word) # get은 위험하지만 있다는게 확실하니 써도 되겠지
                    # else:
                    #     hashtag = HashTag.objects.create(content=word)
                    # try:
                    #     hastag = HashTag.objects.get(content=word)
                    # except:
                    #     hashtag = HashTag.objects.create(content=word)
                    # 위의 두 방법도 돌아는 가겠지만 더 좋은 장고 기능이 있다
                    hashtag, created = HashTag.objects.get_or_create(content=word)  # (object, created) 튜플을 return한다
                    article.hashtags.add(hashtag)

            return redirect('articles:detail', article.pk)
    else:
    # GET 요청 처리 -> form 만 주는거
        article_form = ArticleForm()
    # GET -> 비어있는 Form context
    # POST -> 검증실패시 에러메시지와 입력값 채워진 Form context
    context = {
        'article_form':article_form
    }
    return render(request, 'articles/form.html', context)


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
    # if article.user != request.user:
    #     messages.success(request, '유저정보가 일치하지 않습니다.')
    #     return redirect('articles:detail', article_pk)
    # else:   
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, instance=article)
            if article_form.is_valid():
                # article.title = article_form.cleaned_data.get('title')
                # article.content = article_form.cleaned_data.get('content')
                # article.save()
                article = article_form.save()
                article.hashtags.clear()  # 해시태그 다 삭제하고 다시 태그 등록 과정 한다.
                for word in article.content.split():
                    if word.startswith('#'):
                        hashtag, created = HashTag.objects.get_or_create(content=word)
                        article.hashtags.add(hashtag)                
                return redirect('articles:detail', article_pk)
        else:
            # article_form = ArticleForm(
            #     initial={
            #         'title':article.title,
            #         'content':article.content
            #     }
            # )
            article_form = ArticleForm(instance=article)
        context = {
            # 'article':article,
            'article_form':article_form
        }
        return render(request, 'articles/form.html', context)    
    else:
        raise PermissionDenied  


@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user != request.user:
        messages.success(request, '유저정보가 일치하지 않습니다.')
        return redirect('articles:detail', article_pk)
    else:       
    # if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    # else: # 이렇게하면 포스트 요청으로만 지울 수 있으니까 주소창에서 ~/123/delete 이렇게 적는다고 지워지지 않겠지
    #     return redirect('articles:detail', article.pk)

# def edit(request, article_pk):
#     article = Article.objects.get(pk=article_pk)
#     context = {
#         'article': article
#     }
#     return render(request, 'articles/edit.html', context)


@require_POST
# @login_required  << 이거 까지 쓰면 POST요청으로 인해 오류가 뜬다. 그러니 is_authenticated를 이용한다
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        #1. modelform에 사용자 입력값 넣고
        comment_form = CommentForm(request.POST)
        #2. 검증하고
        if comment_form.is_valid():
        #3. 맞으면 저장
            #3-1. 사용자 입력값으로 comment instace 생성 (저장은 하지않는다!) (아직 데이터베이스에 요청 X)
            comment = comment_form.save(commit=False)
            #3-2. FK 넣고 저장!
            comment.article = article
            comment.user = request.user
            comment.save()
        else:
            messages.success(request, '댓글이 형식에 맞지 않습니다.')
        #4. return redirect
        return redirect('articles:detail',article_pk)
    else:
        return HttpResponse('Unauthorized 로그인하거라',status=401)
    # comment = Comment()
    # comment.content = request.POST.get('comment')
    # comment.article_id = article_pk 
    # comment.save()
    # messages.add_message(request, messages.SUCCESS, '댓글이 등록되었습니다.')
    # return redirect('articles:detail', article_pk)

@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
        # messages.add_message(request, messages.SUCCESS, '댓글이 삭제되었습니다.') 이거도 되지만 밑에 거가 shortcut
        messages.success(request, '댓글이 삭제되었습니다.')
        return redirect('articles:detail', article_pk)
    else:
        # PermissionDenied 이랑 HttpResponseForbidden 이랑 비슷. raise가 어색하니 return으로 통일하게 HttpResponseForbidden으로 하자
        return  HttpResponseForbidden()

@login_required # 함수내에서 request.user를 쓰게 되면 로그인 확인 처리 하는거 잊지말아라!!!!!!!!!!!
def like(request, article_pk):
    article = Article.objects.get(id=article_pk)
    # 좋아요를 누른적이 있다면?
    if request.user in article.like_users.all():
        #좋아요 취소 로직
        article.like_users.remove(request.user)
    # 아니면
    else:
        #좋아요 로직
        article.like_users.add(request.user)
    return  redirect('articles:detail', article_pk)
    

def hashtag(request, hashtag_pk):
    hashtag = get_object_or_404(HashTag, id=hashtag_pk)
    context = {
        'hashtag': hashtag
    }
    return render(request, 'articles/hashtags.html', context)