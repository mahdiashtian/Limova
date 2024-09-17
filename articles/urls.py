# urls.py
from django.urls import path

from articles.views import ArticleList,ArticleDetail

app_name = 'articles'
urlpatterns = [
    path("", ArticleList.as_view(), name="article-list"),
    path("<pk>/", ArticleDetail.as_view(), name="article-detail"),
]
