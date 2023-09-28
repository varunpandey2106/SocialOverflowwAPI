from django.contrib import admin
from .models import Article, ArticleVote, ArticleComment

# Register your models here.

admin.site.register(Article)
admin.site.register(ArticleVote)
admin.site.register(ArticleComment)
