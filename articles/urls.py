from django.urls import path

from . import views



app_name = 'articles'  #이거를 해줘야 다른 앱에서 같은 name을 써도 내가 원하는 곳으로 갈수있겠지
urlpatterns = [
    path('',views.index, name='index'),
    # path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    # path('<int:article_pk>/edit/', views.edit, name='edit'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/comment_create/', views.comment_create, name='comment_create'),
    # path('<int:comment_pk>/comment_delete/', views.comment_delete, name='comment_delete'), 이렇게 해도 되지만 그냥 의미를 담을겸 밑에처럼 해보자
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:article_pk>/like/', views.like, name = 'like') # user_id, article_id 모두 필요하지만 user_id는 request에 있을 테니 article_pk 만 넘겼다
]
