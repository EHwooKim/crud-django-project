from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    # # 위젯 설정 2.
    title = forms.CharField(
        max_length=140, 
        label='제목',
        help_text='제목 입력해!',
        widget=forms.TextInput(
            attrs={
                'placeholder':'제목입력하거라'
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'placeholder':'내용입력'
            }
        )
    )
    # 데이터에 대한 데이터
    class Meta:
        model = Article
        exclude = ('user',)
        # 위젯 설정 1.
        # widgets = {
        #     'title':forms.TextInput(
        #         attrs={
        #             'placeholder': '제목을 입력바랍니다.'
        #         }
        #     )
        # }
        # 아래처럼 원하는 것만 뽑을 수도 있다.
        # fields = ('title',)
        # exclude - ('title', ) 처럼 써서  필요없는거 뺼 수도 있다
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('article','user',)


# 처음에는 이렇게 배웠지. 그런데 하고보니 model 정보를 받와와서 할 수 있을거 같아!!
# class ArticleForm(forms.Form):
#     title = forms.CharField(
#         max_length=140, 
#         label='제목',
#         widget=forms.TextInput(
#             attrs={
#                 'placeholder':'제목입력하거라'
#             }
#         )
#     )
#     content = forms.CharField(
#         # label 내용 수정
#         label='내용',
#         # Django form 에서 html 속성 지정 -> widget
#         widget=forms.Textarea(
#             attrs={
#                 'class':'my-content',
#                 'placeholder':'내용을 입력하세요',
#                 'row':5,
#                 'cols':60,
#             }
#         )
#     )