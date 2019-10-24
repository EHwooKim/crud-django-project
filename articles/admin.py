from django.contrib import admin

# Register your models here.  # 너의 모델을 등록해라
from .models import Article, Comment, HashTag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'updated_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'article')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(HashTag)